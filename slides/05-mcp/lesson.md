## Module 5: MCP "10x Google Fu" (1.25 hrs) ⭐ KEY MODULE

### Learning Objectives
- Understand MCP (Model Context Protocol) documentation servers
- Configure MCP servers for Strands, AWS, and web search
- Experience the "10x Google Fu" skill in action
- Enhance `api-advisor` with MCP documentation access

> **This is THE KEY skill that differentiates Course 4.** The skill of efficiently accessing documentation transfers to ANY project, ANY technology.

---

### 5.1 The Problem with Traditional Documentation Lookup (15 min)

**Concept:** Understand why traditional documentation lookup is slow and inefficient.

#### The Old Way

```
┌──────────────────────────────────────────────────────────────────┐
│              TRADITIONAL DOCUMENTATION LOOKUP                     │
│                                                                   │
│   1. Have a question                                              │
│      "How do I add streaming to my Strands agent?"               │
│                                                                   │
│   2. Open browser                                                 │
│                                                                   │
│   3. Google: "strands agents streaming python"                   │
│      → 10 results of varying quality                             │
│      → Stack Overflow answer from 2023 (might be outdated)       │
│      → Blog post that uses different version                     │
│      → GitHub issue that's unresolved                            │
│                                                                   │
│   4. Click first result... not quite right                       │
│   5. Click second result... different framework                  │
│   6. Click third result... finally official docs!                │
│   7. Navigate to right section...                                │
│   8. Find the answer                                             │
│                                                                   │
│   Time elapsed: 5-15 minutes                                     │
│   Confidence in answer: Medium                                   │
│   Tabs open: 7                                                   │
└──────────────────────────────────────────────────────────────────┘
```

#### Common Frustrations

| Frustration | Why It Happens |
|-------------|----------------|
| **Outdated answers** | Stack Overflow answers from 2 years ago |
| **Wrong version** | Tutorial uses v1, you're on v3 |
| **Context switching** | Jump between 10 tabs |
| **Information overload** | Too many results, hard to filter |
| **No citation** | ChatGPT might hallucinate the answer |

> 💡 **Progressive Disclosure:** You don't memorize documentation. You need to know how to ACCESS it efficiently. This is the skill.

---

### 5.2 How MCP Documentation Servers Work (20 min)

**Concept:** Understand the Model Context Protocol for documentation access.

#### What is MCP?

**MCP (Model Context Protocol)** is a standard for connecting AI models to external data sources — including documentation.

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOW MCP WORKS                                 │
│                                                                  │
│   Your Question              MCP Server              Result      │
│   ─────────────              ──────────              ──────      │
│                                                                  │
│   "How do I add a        →   Strands MCP     →    Exact code    │
│    tool to my agent?"        Server               example from  │
│                              ↓                    official docs  │
│                              Searches Strands     with citation  │
│                              documentation                       │
│                              directly                            │
│                                                                  │
│   The MCP server has direct access to:                          │
│   • Official documentation (always current)                      │
│   • Code examples (tested and working)                          │
│   • API references (accurate signatures)                         │
│                                                                  │
│   NOT searching the general web                                 │
│   NOT using cached/outdated data                                │
│   NOT hallucinating from training data                          │
└─────────────────────────────────────────────────────────────────┘
```

#### MCP Server Types

| Server Type | Purpose | Example |
|-------------|---------|---------|
| **Documentation** | Access official docs | strands-agents, aws-docs |
| **Filesystem** | Read project files | @modelcontextprotocol/server-filesystem |
| **Web Search** | Fallback to web | brave-search MCP |
| **Database** | Query data | PostgreSQL MCP |

#### The "10x Google Fu" Effect

```
Traditional Way:
  Google → 10 results → click → read → back → click → read → ...
  Time: 5-15 minutes
  Confidence: ???

MCP Way:
  Question → MCP Server → Answer with citation
  Time: 10-30 seconds
  Confidence: High (official docs)
```

> 🏢 **Enterprise Context:** In enterprise, you work with dozens of APIs — internal services, cloud providers, frameworks. This skill scales. Set up MCP for your internal docs, and your whole team benefits.

---

### 5.3 Configuring MCP Servers (20 min)

**Concept:** Set up MCP servers for Strands, AWS, and web search.

#### MCP Server Configuration

```json
// .vscode/mcp.json (or ~/.config/mcp/config.json)
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "description": "Read project files"
    },
    
    "strands-agents": {
      "command": "uvx",
      "args": ["strands-agents-mcp-server"],
      "autoApprove": ["search_strands_docs", "get_strands_example"],
      "description": "Strands Agents official documentation"
    },
    
    "aws-docs": {
      "command": "uvx", 
      "args": ["awslabs.aws-documentation-mcp-server"],
      "autoApprove": ["search_documentation", "get_documentation"],
      "description": "AWS official documentation"
    },
    
    "web-search": {
      "command": "uvx",
      "args": ["mcp-server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      },
      "autoApprove": ["brave_web_search"],
      "description": "Web search fallback when docs don't have answer"
    }
  }
}
```

#### Server Selection Strategy

| Question Type | MCP Server | Why |
|---------------|------------|-----|
| Strands syntax, patterns | strands-agents | Official Strands docs |
| AWS services, configuration | aws-docs | Official AWS docs |
| Flask patterns | filesystem | Read existing routes in project |
| Course 3 integration | filesystem | Read api-contract.yaml |
| General/unknown | web-search | Fallback for anything else |

#### Testing MCP Servers

```bash
# Test strands-agents MCP
mcp call strands-agents search_strands_docs --query "tool decorator"

# Test aws-docs MCP  
mcp call aws-docs search_documentation --query "Lambda timeout configuration"

# Test filesystem
mcp call filesystem list_files --path "src/routes"
```

**Hands-On:**
- Create `.vscode/mcp.json` (or equivalent for your editor)
- Install MCP servers:
  ```bash
  pip install strands-agents-mcp-server
  pip install awslabs.aws-documentation-mcp-server
  pip install mcp-server-brave-search
  ```
- Test each server with a simple query
- Verify you get documentation responses (not web search results)

[📸 Screenshot: MCP server configuration in VS Code]

---

### 5.4 The API-Advisor with MCP Integration (20 min)

**Concept:** Enhance the `api-advisor` agent with MCP documentation access.

#### Agent Definition

```yaml
# .github/skills/api-advisor/SKILL.md
---
name: api-advisor
description: Teaching + documentation access via MCP — "10x Google Fu"
tools:
  - read
  - search
  - fetch
  - mcp:strands-agents
  - mcp:aws-docs
  - mcp:web-search
model_tier: balanced  # Teaching requires nuanced responses
---

# API Advisor Agent

## Role
Guide humans through API development decisions.
Use MCP to access documentation in real-time — never guess, always cite.

**Philosophy:** You don't memorize documentation. You ACCESS it efficiently.

## Capabilities
- Explain API concepts and architectural patterns
- Access Strands documentation via MCP (official, current)
- Access AWS documentation via MCP (official, current)
- Fall back to web search when specific docs don't have the answer
- Read project files for context (existing code, specs, history)

## Restrictions
- Cannot modify files (Advisor, not Doer)
- Cannot make external API calls
- MUST cite documentation sources — never claim knowledge you don't have
- If unsure, say so and suggest where to look

## MCP Usage Pattern

1. Human asks question
2. Determine which MCP server is most relevant
3. Search that documentation
4. Synthesize answer WITH citation
5. Offer to explain further or dive deeper

**Always cite your sources.** Example:
"According to the Strands documentation (tools.md), you can..."

## Progressive Disclosure Hints

When the human asks about specific topics, use the appropriate source:

| Topic | Source | Action |
|-------|--------|--------|
| Strands agent patterns | mcp:strands-agents | search_strands_docs |
| Strands tool creation | mcp:strands-agents | get_strands_example |
| AWS Lambda config | mcp:aws-docs | search_documentation |
| AWS API Gateway | mcp:aws-docs | search_documentation |
| Flask patterns | filesystem | Read src/routes/ for conventions |
| Model integration | filesystem | Read docs/api-contract.yaml |
| Feature validation | filesystem | Read docs/feature_schema.yaml |
| Deployment options | mcp:aws-docs | Compare Lambda vs ECS |
| General questions | mcp:web-search | brave_web_search |

## Example Interactions

### Strands Question
```
Human: "How do I add streaming to my Strands agent?"

api-advisor:
1. Uses mcp:strands-agents to search "streaming"
2. Finds streaming.md in official docs
3. Returns:

"According to the Strands documentation (streaming.md), you enable 
streaming by setting `stream=True` in the agent configuration:

```python
agent = Agent(
    name="my-agent",
    model="anthropic/claude-3-haiku",
    stream=True  # Enable streaming
)
```

The response will be an async generator you can iterate over.
Would you like me to show how to handle the streamed response in Flask?"
```

### AWS Question
```
Human: "What's the default timeout for API Gateway?"

api-advisor:
1. Uses mcp:aws-docs to search "API Gateway timeout"
2. Returns:

"According to AWS documentation (API Gateway Developer Guide), 
API Gateway has a 29-second maximum integration timeout. This is 
a hard limit and cannot be increased.

For your /insights endpoint with a 30-second agent timeout, you'll 
need to either:
1. Reduce agent timeout to 25 seconds (leaving buffer)
2. Use asynchronous invocation pattern
3. Consider a different architecture

Want me to explain the async pattern?"
```

### Project Context Question
```
Human: "What does Course 3's model expect as input?"

api-advisor:
1. Uses filesystem to read docs/feature_schema.yaml
2. Returns:

"Looking at feature_schema.yaml from Course 3, the FraudPredictor 
expects these features:

Required:
- amount (float): Transaction amount
- merchant_category (string): Category code

Optional:
- time_since_last (integer): Seconds since last transaction
- ...

The full schema is in docs/feature_schema.yaml. Your /predict 
endpoint should validate against this before calling the model."
```

## Handoffs

- Receives from: Human (questions), strands-builder (architectural guidance)
- Hands off to: endpoint-generator (when ready to implement)
- Hands off to: strands-builder (when creating new agents)

## What I Don't Do

- Modify code (hand off to Doer agents)
- Guess when I don't know (use MCP or say "I'm not sure")
- Provide outdated information (always use MCP for current docs)
```

> 💡 **Progressive Disclosure:** Notice the agent has a clear table of "where to look for what." This is progressive disclosure in action — the agent doesn't load all documentation upfront. It accesses what's needed when needed.

**Hands-On:**
- Create/update `.github/skills/api-advisor/SKILL.md`
- Test with Strands question: "How do I add a tool to my Strands agent?"
- Verify MCP is used (check for citation)
- Test with AWS question: "What's the Lambda memory limit?"
- Test with project question: "What's in my OpenAPI spec?"

[📸 Screenshot: api-advisor using MCP to answer with citations]

---

### 5.5 Building the "10x Google Fu" Habit (10 min)

**Concept:** Learn to use this skill consistently in your development workflow.

#### The Habit Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                THE 10x GOOGLE FU HABIT                           │
│                                                                  │
│   1. RECOGNIZE the trigger                                       │
│      "I need to know how to..."                                 │
│      "What's the syntax for..."                                 │
│      "Does this framework support..."                           │
│                                                                  │
│   2. RESIST the old habit                                       │
│      Don't open browser                                         │
│      Don't Google it                                            │
│      Don't ask ChatGPT without context                         │
│                                                                  │
│   3. USE the api-advisor                                        │
│      "api-advisor, how do I add streaming to Strands?"         │
│      Let it use MCP                                             │
│      Get cited answer                                           │
│                                                                  │
│   4. VERIFY if needed                                           │
│      MCP gives you the source                                   │
│      Click through to verify if critical                        │
│      Usually not needed — it's official docs                   │
└─────────────────────────────────────────────────────────────────┘
```

#### When to Use Each Approach

| Situation | Approach | Why |
|-----------|----------|-----|
| Framework syntax question | api-advisor with MCP | Fastest, most accurate |
| Debugging specific error | api-advisor + error context | Can read your code too |
| Comparing options | api-advisor | Can search multiple docs |
| Very new technology | Web search fallback | MCP might not exist yet |
| Internal company docs | Create custom MCP server | Same pattern, your data |

#### The Transferable Skill

This skill transfers to ANY technology:

| Technology | MCP Approach |
|------------|--------------|
| New framework (e.g., FastAPI) | Find/create MCP server for its docs |
| Cloud provider (e.g., GCP) | Use GCP documentation MCP |
| Internal systems | Create MCP server indexing internal docs |
| Legacy codebase | Create MCP server that indexes the code |

> 🏢 **Enterprise Context:** The highest-leverage thing you can do for your team is set up MCP servers for your internal documentation. Every developer's questions get answered faster.

**Hands-On:**
- Practice 5 different questions using api-advisor with MCP
- Time each one (target: under 60 seconds)
- Note the citations in each response
- Compare to what Google search would have taken

[🎬 Video: Querying documentation via MCP in real-time]

---

### Module 5 Checkpoint

**By end of Module 5, you have:**
- ✅ MCP servers configured for Strands, AWS, web search
- ✅ `api-advisor` enhanced with MCP documentation access
- ✅ Practiced the "10x Google Fu" skill
- ✅ Understanding of when/how to use each MCP server

**The Key Skill:**
> **You don't memorize documentation. You know how to ACCESS it efficiently.**

**Git tag:** `module-5-mcp`

**HISTORY.md Entry:**
```markdown
## Module 5 Complete ⭐ KEY MODULE

### Key Skill Acquired
"10x Google Fu" — accessing documentation efficiently via MCP

### Configured MCP Servers
- strands-agents: Strands official documentation
- aws-docs: AWS official documentation  
- web-search: Fallback for general questions
- filesystem: Project files and specs

### api-advisor Enhancement
- Now uses MCP for all documentation questions
- Responses include citations to official sources
- Progressive disclosure table guides source selection

### Habit Established
Question → api-advisor → MCP → Cited Answer
(Not: Question → Google → 10 tabs → Maybe find answer)

### Next: Module 6 — CDK Introduction
```

---

