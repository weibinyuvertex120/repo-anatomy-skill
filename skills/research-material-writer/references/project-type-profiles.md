# Project Type Profiles

Use this reference after the research brief and before collecting broad evidence. Its purpose is to identify the information that changes whether a reader can understand, try, and adopt a project. It is a routing guide, not eight templates to stack into every document.

## Classification Rule

Select one primary type by asking which interface the intended user directly operates to obtain value. Add at most one secondary type when a separate interface changes the setup, safety boundary, or verification method.

Use these values in working notes and evaluation records:

- `cli_or_local_tool`
- `library_or_sdk`
- `api_or_hosted_service`
- `plugin_or_extension`
- `agent_skill_or_mcp`
- `model`
- `dataset_or_resource_collection`
- `service_application`

Do not create a `mixed` type. For a multi-interface project, select the interface that governs the reader's adoption decision as the primary type and add at most one distinct secondary type. If classification changes the safe first-use path and evidence is insufficient, ask one targeted question. Otherwise state the classification and bounded assumption. Do not add every profile because the repository contains multiple components.

## Shared Understanding Map

Before detailed setup, explain the project through a compact understanding map:

1. **Problem and user:** the practical problem, intended user, and when the project is unnecessary.
2. **Input:** data, request, file, event, code, prompt, or user action entering the project.
3. **Processing:** the transformation, decision, orchestration, storage, or execution performed.
4. **Output:** the artifact, response, state change, capability, or user-visible result.
5. **Core components:** only the components needed to understand the first workflow.
6. **Flow:** how control, data, credentials, and responsibility move between components.
7. **Responsibility boundary:** what the project owns, what the host or caller owns, and what remains an external dependency.
8. **First success:** the smallest useful and observable outcome.

Use a short flow, table, or diagram only when it reduces explanation. Do not turn the map into a complete architecture reference.

## CLI Or Local Tool

The reader must understand:

- executable or entry point, accepted input, processing, and output;
- installation scope, working directory, files or processes touched, and whether elevated permission is required;
- configuration precedence, exit status, logs, generated artifacts, cleanup, and repeatability;
- batch, network, destructive, or irreversible behavior that differs from the minimum path.

Prefer evidence from release artifacts, package metadata, command help, source entry points, tests, configuration schema, and security guidance.

Minimum practice:

- use a pinned version and controlled local input;
- run one narrow command;
- inspect the output artifact, state, or status rather than relying on absence of errors;
- verify one meaningful failure, refusal, cleanup, or exit-status boundary.

Transfer task: change one input or option, predict the effect, then verify it.

## Library Or SDK

The reader must understand:

- public API surface, initialization and lifecycle;
- input, return, error, concurrency, and side-effect contracts;
- runtime and dependency compatibility;
- stable, experimental, deprecated, and internal interfaces;
- versioning policy, migration path, and whether published compatibility claims are reliable.

Prefer evidence from generated API reference, source declarations, type definitions, package metadata, tests, changelog, migration guides, and release policy. Semantic Versioning is evidence only when the project declares a public API and follows it.

Minimum practice:

- install a pinned version in an isolated environment;
- call one public API with a controlled input;
- inspect the returned value and one documented exception or invalid-input behavior;
- record imports, configuration, version, and dependency scope.

Transfer task: modify the input or compose a second public API without copying the original example verbatim.

## API Or Hosted Service

The reader must understand:

- service identity, environment or server URL, versioning, and availability scope;
- authentication, authorization, credential placement, and minimum permission;
- operation, parameters, request body, response body, status, headers, and error contract;
- pagination, limits, retries, idempotency, pricing, regional constraints, data retention, and external processing;
- whether a client library changes but does not replace the underlying service contract.

Prefer evidence from the current API specification, endpoint reference, authentication guide, service limits, status page, pricing or policy page, SDK source, and official examples. For HTTP APIs, use the OpenAPI operation, parameter, request, response, server, and security model when available.

Minimum practice:

- begin with a read-only or reversible request using minimum authorization;
- inspect status, relevant headers, and body;
- verify one bounded error, permission denial, pagination, or limit behavior;
- never expose a real credential in examples, logs, or feedback records.

Transfer task: change one parameter or endpoint and explain the expected response before making the request.

## Plugin Or Extension

The reader must understand:

- canonical extension identity, publisher, release channel, and host version range;
- desktop, web, remote, or workspace execution location;
- activation conditions, code entry points, contribution points, settings, commands, and dependencies;
- workspace trust, virtual workspace, organization policy, telemetry, update, disable, and uninstall behavior;
- which capabilities come from the host rather than the extension itself.

Prefer evidence from the official marketplace, extension manifest, host extension specification, source entry points, activation tests, settings schema, and trust documentation.

Minimum practice:

- use a bounded host profile or disposable workspace;
- confirm installation and discovery;
- trigger one declared contribution point and observe its effect;
- verify a disabled, unsupported, restricted, or permission-limited state.

Transfer task: use the same contribution point in a second representative file or workspace context.

## Agent Skill Or MCP Integration

The reader must understand:

- host, client, server, Skill, model, and user roles that actually exist in the target system;
- discovery, explicit selection, loading, capability negotiation, and version identity;
- resources, prompts, tools, instructions, inputs, outputs, and data flow;
- user consent, tool approval, credentials, roots or workspace scope, network access, logging, and trace visibility;
- the difference between behavioral instructions and enforced permission boundaries;
- session state, cross-session memory, external knowledge, and persistence as separate concerns.

Prefer evidence from the host and protocol specification, package manifest, observable discovery or loading events, capability lists, tool schema, permission settings, trace, and controlled calls. A good answer that mentions the Skill name is not proof that the Skill loaded.

Minimum practice:

- confirm artifact identity and discovery or explicit loading when observable;
- invoke one read-only capability with controlled data;
- preserve the available trace or evidence chain;
- verify one denied, unavailable, or consent-gated action without requesting broader permission.

Transfer task: apply the capability to a second bounded task while preserving the same permission constraints.

## Model

The reader must understand:

- model identity, base-model relationship, architecture class, task, version, and license;
- intended use, out-of-scope use, target users, input and output contract, and human-review requirement;
- training or fine-tuning data, coverage, provenance, processing, and known data gaps;
- evaluation tasks, datasets, metrics, baselines, reproducibility, and whether claims are project-authored;
- bias, safety, privacy, misuse, compute, latency, deployment, quantization, and hardware constraints.

Prefer evidence from the model card, configuration, code, paper, dataset cards, license, evaluation scripts, benchmark records, safety report, and reproducible inference. A benchmark score does not prove suitability for the reader's use case.

Minimum practice:

- pin the model and runtime configuration;
- run or inspect one recorded inference with controlled input;
- evaluate the output against an explicit criterion;
- test or disclose one known failure mode, uncovered population, unsafe use, or evaluation gap.

Transfer task: use a second intended-domain input and compare it with the same acceptance criterion.

## Dataset Or Resource Collection

The reader must understand:

- motivation, creator, intended consumer, unit of data or entry, and project scope;
- composition, schema or classification, collection or curation, preprocessing, version, and provenance;
- license, consent, privacy, sensitive content, redistribution, and attribution requirements;
- recommended and prohibited uses, coverage gaps, representativeness, staleness, and maintenance;
- access method, size, integrity, update frequency, and downstream transformations.

Prefer evidence from a datasheet or data card, repository and release metadata, schema, sample records, collection methodology, license, checksums, maintenance policy, and issue history. For resource collections, verify entries rather than treating inclusion as endorsement.

Minimum practice:

- inspect representative records or entries;
- validate the schema, classification, provenance, or integrity signal;
- use one item in a bounded task;
- verify one coverage gap, stale entry, missing field, prohibited use, or licensing constraint.

Transfer task: select a new item through the documented classification and justify its fit.

## Service Application

The reader must understand:

- codebase and deploy relationship;
- explicit and isolated dependencies;
- configuration, secrets, backing services, and environment differences;
- build, release, and run stages;
- process model, port or interface, concurrency, state, startup, shutdown, and disposability;
- logs, health, metrics, migrations, management tasks, scaling, backup, rollback, and operational owner.

Prefer evidence from deployment manifests, dependency and lock files, configuration schema, container or process definitions, health endpoints, observability setup, CI/CD, runbooks, migration scripts, and incident or support guidance.

Minimum practice:

- start one pinned deployment in an isolated environment;
- verify health, logs, and one useful request;
- verify missing configuration, dependency unavailability, graceful shutdown, or rollback;
- keep production data, credentials, and irreversible migrations outside the first path.

Transfer task: change one non-secret configuration value and verify the documented operational effect.

## Mixed Projects

Use a primary and secondary profile when one user journey crosses two interfaces, for example:

- a library with a hosted API;
- a CLI that starts a service;
- an MCP server distributed as an editor extension;
- a model delivered through a hosted inference API.

State which profile governs each stage. Do not duplicate shared identity, risk, or source sections. If more than two profiles appear necessary, narrow the reader's target workflow before continuing.

## Type-Aware Quality Gate

Before drafting, confirm:

- the primary type follows the reader's direct interface, not repository labels;
- the understanding map explains input, processing, output, flow, boundary, and first success;
- the evidence plan includes type-specific authoritative artifacts;
- the first practice tests the project's actual value, not only installation;
- one type-specific boundary is observable or explicitly blocked;
- one transfer task demonstrates use beyond copying;
- unrelated profiles have not been added for completeness.
