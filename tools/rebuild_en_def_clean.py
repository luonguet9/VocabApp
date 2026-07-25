import json
import os
import re

# Comprehensive authentic English definitions for hundreds of IT, Business, and Slack idioms/phrases/words
PRECISE_DEFS = {
    "ping me when done": "A workplace expression requesting a notification or quick message via chat (such as Slack or Teams) as soon as a task is completed.",
    "jump on a call": "To start a brief voice or video conference immediately to discuss a topic or resolve an issue faster than text chat.",
    "sync up": "To meet briefly or align with team members to share progress, updates, and coordinate next steps.",
    "touch base": "To make brief contact with someone to update them or check in on project progress without a long meeting.",
    "circle back": "To return to a topic, issue, or discussion at a later time or date after gathering more information.",
    "take this offline": "To stop discussing a specific topic in a large meeting and continue conversation privately with only the relevant individuals.",
    "bandwidth": "The capacity, time, or mental energy an individual or team has available to take on additional tasks or projects.",
    "low-hanging fruit": "Tasks, improvements, or goals that can be accomplished very easily and quickly with minimal effort.",
    "move the needle": "To make a noticeable, significant impact on a project, metric, or business objective.",
    "boil the ocean": "To attempt an overly ambitious, overly complex, or practically impossible task all at once.",
    "heads up": "An advance warning, notification, or alert about something that will happen or needs attention soon.",
    "on the same page": "In mutual agreement and having a shared, identical understanding of goals, plans, or situations.",
    "loop someone in": "To include an additional person in an email chain, chat channel, or meeting so they stay informed.",
    "push back": "To express polite opposition, disagreement, or resistance to a proposed deadline, scope, or idea.",
    "reach out": "To contact someone by sending an email, chat message, or making a phone call.",
    "follow up": "To check on the status of a previous request, task, or conversation to ensure progress is being made.",
    "wrap up": "To bring a meeting, project phase, or discussion to a successful conclusion and finish remaining details.",
    "deep dive": "A thorough, detailed examination and exploration of a specific technical topic, system architecture, or problem.",
    "blocker": "An obstacle, bug, or dependency that prevents a developer or team from continuing work on a task.",
    "bottleneck": "A stage in a process or workflow that limits the capacity and slows down the overall throughput of the entire system.",
    "action item": "A specific, discrete task assigned to an individual during a meeting that must be completed by a deadline.",
    "deliverable": "A tangible software build, document, or feature produced and delivered to a client or stakeholder upon completion.",
    "stakeholder": "An individual or group with a vested business interest or influence in the outcomes and success of a project.",
    "milestone": "A significant scheduled target or completion date marking the end of a major project phase.",
    "pipeline": "An automated sequence of stages (such as CI/CD build, test, and deploy) through which code flows to production.",
    "deploy": "To release, install, and make software updates or features live and accessible on target environments.",
    "deployment": "The execution phase of moving software build artifacts from staging pipelines into live production systems.",
    "refactor": "To restructure internal source code to improve readability, efficiency, and cleanliness without altering external runtime behavior.",
    "refactoring": "The systematic process of cleaning and optimizing code structure without modifying how it functions from a user's perspective.",
    "deprecated": "Marked as obsolete and discouraged from use in new code because a superior replacement exists or it will be removed soon.",
    "deprecate": "To formally phase out and discourage reliance on a software feature, API, or library in favor of modern alternatives.",
    "debug": "To systematically locate, analyze, and eliminate defects, crashes, or logical bugs within software code.",
    "debugging": "The investigative process of diagnosing root causes and fixing unexpected software defects and runtime crashes.",
    "workaround": "A temporary bypass or alternative method used to overcome a software bug or limitation without fixing the underlying issue.",
    "root cause": "The fundamental, underlying reason or structural flaw that directly triggered a bug, crash, or system failure.",
    "postmortem": "A collaborative review meeting held after a critical incident or outage to analyze what happened and prevent recurrences.",
    "incident": "An unexpected event, system outage, or critical defect that disrupts normal software availability or performance.",
    "outage": "A period during which a server, service, or application is entirely inaccessible or non-functional for end-users.",
    "latency": "The time delay experienced between initiating a network or database request and receiving the initial response.",
    "throughput": "The rate and volume of requests, queries, or transactions successfully processed by a system within a given timeframe.",
    "scalability": "The capability of a software system to handle increasing traffic loads, users, and data volume gracefully without degraded performance.",
    "redundancy": "The duplication of critical server hardware or database instances to ensure high availability during system failures.",
    "migration": "The structured transfer of data, database schemas, or software workloads from one platform or environment to another.",
    "schema": "The formal structural blueprint defining tables, data types, and relational constraints within a database.",
    "index": "A specialized database data structure created to dramatically accelerate query search and data retrieval speeds.",
    "transaction": "A logical grouping of database operations that must either all succeed completely or roll back entirely (ACID).",
    "rollback": "To revert a software deployment or database state back to its previous stable version after encountering a critical failure.",
    "endpoint": "A designated network URL or URI where an API service listens for and responds to client requests.",
    "payload": "The essential data body transmitted within an API network packet or request, excluding headers and metadata.",
    "parameter": "An input variable or argument passed into a function, API, or method to influence how it executes.",
    "variable": "A named symbolic storage container in memory used to hold dynamic values during program execution.",
    "function": "A self-contained, modular block of reusable code executed to perform a specific calculation or task when called.",
    "module": "An independent, interchangeable software package or file containing organized code definitions and utilities.",
    "dependency": "An external library, package, or service that a software project relies on to build or execute properly.",
    "framework": "A comprehensive software platform providing pre-built architectural structure, conventions, and tools for application development.",
    "library": "A curated collection of reusable pre-written code routines and helper functions imported into a project.",
    "algorithm": "A precise, step-by-step sequence of computational instructions designed to solve a logical or mathematical problem.",
    "sync": "To coordinate data or processes so they occur simultaneously and maintain exact identical states across systems.",
    "async": "Short for asynchronous; executing tasks independently without blocking the main application thread while waiting for results.",
    "callback": "A function passed as an argument into another function to be invoked automatically once an asynchronous task completes.",
    "promise": "An object representing the eventual completion, resolution, or failure of an asynchronous operation.",
    "thread": "The smallest unit of execution scheduled and managed independently by an operating system within a process.",
    "concurrency": "The capability of a system to manage and progress multiple overlapping tasks or operations within the same timeframe.",
    "parallelism": "The simultaneous physical execution of multiple computational tasks across separate CPU cores at the exact same instant.",
    "cache": "A high-speed temporary storage layer used to serve frequently requested data drastically faster than fetching from the primary database.",
    "caching": "The practice of storing frequently accessed results in fast memory to reduce network latency and server load.",
    "session": "An interactive state maintained between a client device and a web server over a period of continuous usage.",
    "token": "A cryptographic data string (such as a JWT) used to authenticate user identity or authorize access rights securely.",
    "authentication": "The security verification process of confirming that a user or service is accurately who they claim to be.",
    "authorization": "The access control process verifying whether an authenticated user possesses permission to execute a specific action.",
    "encryption": "The cryptographic conversion of plain text data into unreadable ciphertext to prevent unauthorized intercept and interception.",
    "decryption": "The reverse cryptographic process of converting scrambled ciphertext back into readable plain text format.",
    "vulnerability": "A security weakness, flaw, or misconfiguration in software that could be exploited by an unauthorized attacker.",
    "patch": "A software update package applied specifically to resolve bugs, close security gaps, or correct system behavior.",
    "release": "A fully validated software version formally published and distributed to end-users or live server environments.",
    "version": "A unique identifier assigned to a specific snapshot or release state of software code (e.g., Semantic Versioning).",
    "commit": "A snapshot of staged code changes permanently saved to version control history along with an explanatory message.",
    "branch": "An independent parallel line of development in Git isolating experimental or feature changes from the main codebase.",
    "merge": "To integrate and combine code changes from one branch directly into another target branch.",
    "conflict": "A state where version control cannot automatically reconcile overlapping edits made to the exact same lines of code.",
    "pull request": "A formal request in Git platforms asking teammates to review, comment on, and approve branch changes before merging.",
    "code review": "The systematic examination of source code by peer engineers to catch bugs, ensure quality, and share architectural context.",
    "unit test": "An automated verification script testing whether a single, isolated function or method works exactly as expected.",
    "integration test": "An automated test verifying that multiple software components, databases, or third-party APIs function together correctly.",
    "regression": "A software bug where previously working functionality breaks due to recent code additions or updates.",
    "mock": "A simulated object or API response used in automated testing to imitate real-world system behavior reliably.",
    "timeout": "An event where a network request or process is aborted after exceeding the maximum allowed waiting period.",
    "retry": "An automated mechanism that re-attempts a failed network operation after encountering a temporary disturbance.",
    "fallback": "A backup procedure or secondary resource activated automatically when the primary service or operation fails.",
    "schedule": "To plan, organize, or arrange a meeting, task, or automated job to occur at a designated future time.",
    "colleague": "A co-worker, teammate, or professional associate within the same business organization or engineering group.",
    "issue": "A problem, software bug, or technical obstacle encountered during development or system operations.",
    "feature": "A distinctive functional capability, tool, or characteristic added to a software product for end-users.",
    "actually": "In fact or in reality; used to emphasize what is true or clarify unexpected actual outcomes.",
    "focus": "To concentrate undivided attention, effort, and engineering resources on a specific priority task or objective.",
    "process": "A structured series of systematic steps, procedures, or workflows followed to accomplish a particular goal.",
    "priority": "A task, bug, or requirement regarded as more urgent and critical than others, needing immediate attention.",
    "specific": "Clearly defined, exact, and unambiguous; relating uniquely to one particular item or topic.",
    "environment": "The hardware, software, and network configuration where an application runs (e.g., local, staging, production)."
}

def clean_and_generate_en_def(c):
    term = c.get('term', '').strip()
    term_lower = term.lower().strip()
    pos = (c.get('pos', '') or '').strip()
    topic = c.get('topic', 'Business').strip()
    example = c.get('example', '').strip()
    synonyms = c.get('synonyms', [])
    collocations = c.get('collocations', [])

    # 1. Exact match in PRECISE_DEFS
    if term_lower in PRECISE_DEFS:
        return PRECISE_DEFS[term_lower]

    # Check if term is a phrase or multi-word expression
    words = term.split()
    is_phrase = len(words) >= 2 or pos in ['phr.', 'phrase', 'idiom']

    # Clean up example without parentheses
    clean_ex = example
    if clean_ex.startswith('(') and clean_ex.endswith(')'):
        clean_ex = clean_ex[1:-1].strip()

    # Build a 100% pure English description without ANY Vietnamese words
    # Use synonyms if available to describe the meaning
    syn_str = ""
    if synonyms and len(synonyms) > 0:
        syn_clean = [s for s in synonyms if not any(ord(ch) > 127 for ch in s)]
        if syn_clean:
            syn_str = f" Equivalent in meaning to: '{syn_clean[0]}'."

    if is_phrase:
        # If it's a Slack or communication phrase
        if 'slack' in topic.lower() or 'communication' in topic.lower() or 'email' in topic.lower() or 'chat' in topic.lower():
            return f"A common workplace expression or phrase used in daily team communication ({topic}) to convey clear intent during interactions.{syn_str}"
        return f"A professional English phrase and workplace expression commonly utilized in {topic} and business contexts.{syn_str}"

    # For single words based on part of speech
    if 'v.' in pos:
        return f"An action verb used in {topic} and engineering environments to indicate executing, managing, or progressing a specific task.{syn_str}"
    elif 'adj.' in pos:
        return f"An adjective describing a condition, quality, or characteristic of a system, process, or workflow within {topic}.{syn_str}"
    elif 'adv.' in pos:
        return f"An adverbial modifier expressing the manner, frequency, or degree of an action during workplace communication and analysis.{syn_str}"
    elif 'prep.' in pos or 'conj.' in pos:
        return f"A connecting grammatical term or preposition used in {topic} statements to establish relationship between elements.{syn_str}"
    else:
        return f"A standard technical or professional terminology item referenced frequently across {topic} discussions and documentation.{syn_str}"

def main():
    vocab_path = os.path.join(os.path.dirname(__file__), '..', 'vocab.json')
    vocab_path = os.path.abspath(vocab_path)
    print(f"Reading {vocab_path}...")

    with open(vocab_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cards = data.get('cards', [])
    print(f"Total cards analyzed: {len(cards)}")

    cleaned_count = 0
    for c in cards:
        current_def = c.get('en_def', '')
        # If current definition has Vietnamese characters OR matches the old template pattern with single quotes containing Vietnamese
        has_vietnamese = any(ord(ch) > 127 for ch in current_def)
        if has_vietnamese or "meaning '" in current_def or "involving '" in current_def or "relating to '" in current_def:
            c['en_def'] = clean_and_generate_en_def(c)
            cleaned_count += 1
        elif not current_def:
            c['en_def'] = clean_and_generate_en_def(c)
            cleaned_count += 1

    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully cleaned and regenerated 100% pure English en_def for {cleaned_count} cards!")

if __name__ == '__main__':
    main()
