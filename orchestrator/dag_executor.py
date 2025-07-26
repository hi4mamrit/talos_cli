import yaml
from collections import defaultdict, deque

def load_dag_config(yaml_path: str):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def build_dependency_graph(steps):
    graph = defaultdict(list)
    indegree = defaultdict(int)
    step_map = {}

    for step in steps:
        step_id = step['id']
        step_map[step_id] = step
        for dep in step.get('depends_on', []):
            graph[dep].append(step_id)
            indegree[step_id] += 1
        if step_id not in indegree:
            indegree[step_id] = 0

    return graph, indegree, step_map

def topological_sort(graph, indegree):
    q = deque([node for node in indegree if indegree[node] == 0])
    sorted_steps = []
    total_nodes = len(indegree)

    while q:
        node = q.popleft()
        sorted_steps.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                q.append(neighbor)

    # Check for cycles - if we haven't processed all nodes, there's a cycle
    if len(sorted_steps) != total_nodes:
        remaining_nodes = [node for node in indegree if node not in sorted_steps]
        raise ValueError(f"Cycle detected in DAG. Nodes involved in cycle: {remaining_nodes}")

    return sorted_steps

def run_dag_from_yaml(yaml_path: str):
    config = load_dag_config(yaml_path)
    steps = config["steps"]
    graph, indegree, step_map = build_dependency_graph(steps)
    execution_order = topological_sort(graph, indegree)

    step_outputs = {}

    for step_id in execution_order:
        step = step_map[step_id]
        agent = step["agent"]
        print(f"🔧 Running {step_id} → {agent}")

        # Resolve dynamic input references like ${extract_p0.output}
        raw_input = step.get("input", "")
        if isinstance(raw_input, str) and raw_input.startswith("${") and raw_input.endswith("}"):
            ref_content = raw_input[2:-1]  # Remove ${ and }
            
            # Validate the reference format (only allow alphanumeric, underscore, and single dot)
            if not ref_content.replace("_", "").replace(".", "").isalnum() or ref_content.count(".") != 1:
                raise ValueError(f"Invalid reference format: {raw_input}. Expected format: ${{step_id.output}}")
            
            ref_parts = ref_content.split(".")
            dep_id, output_key = ref_parts[0], ref_parts[1]
            
            # Validate that the referenced step exists in our outputs
            if dep_id not in step_outputs:
                raise ValueError(f"Referenced step '{dep_id}' not found in previous outputs")
            
            # Only allow 'output' as the property for security
            if output_key != "output":
                raise ValueError(f"Only 'output' property is allowed, got: {output_key}")
                
            step["input"] = step_outputs.get(dep_id)

        output = run_agent_by_name(agent, step.get("input"), step.get("params", {}))
        step_outputs[step_id] = output

    return step_outputs

def run_agent_by_name(agent_name, input_text, params=None):
    from email_client.fetcher import fetch_recent_emails
    from email_client.task_extractor import extract_p0_tasks
    from orchestrator.agents.summarizer import summarize_p0_tasks
    from orchestrator.agents.helloWorld import HelloWorld
    from utils.discord_notifier import send_discord_message
    from orchestrator.agents.ollama_runner import run_ollama
    
    if agent_name == "gmail_reader":
        return fetch_recent_emails()
    elif agent_name == "gpt_task_extractor":
        return extract_p0_tasks(input_text)
    elif agent_name == "gpt_summarizer":
        return summarize_p0_tasks(input_text)
    elif agent_name == "ollama_agent":
      return run_ollama(input_text, params or {})
    elif agent_name == "file_writer":
        with open("data/p0_digest_summary.txt", "w") as f:
            f.write(input_text)
        return "✅ written to disk"
    elif agent_name == "discord_notifier":
        topic = params.get("topic", "🧠 Daily P0 Digest")
        send_discord_message(topic, input_text)
        return "✅ sent to Discord"
    elif agent_name == "helloWorld":
        return HelloWorld()
    else:
        raise ValueError(f"Unknown agent: {agent_name}")
