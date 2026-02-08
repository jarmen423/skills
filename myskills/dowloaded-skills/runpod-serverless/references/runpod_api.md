# RunPod Serverless API Reference

## GraphQL API Endpoint
`https://api.runpod.io/graphql`

## Authentication
Header: `Authorization: Bearer <YOUR_API_KEY>`

## Common GPU Types (IDs)
- **NVIDIA RTX 3090**: `AMPERE_24`
- **NVIDIA RTX 4090**: `ADA_24`
- **NVIDIA A4000**: `AMPERE_16`
- **NVIDIA A5000**: `AMPERE_24` (Note: similar memory to 3090)
- **NVIDIA A6000**: `AMPERE_48`
- **NVIDIA RTX 6000 Ada**: `ADA_48_PRO`
- **NVIDIA A100 80GB**: `AMPERE_80`
- **NVIDIA H100**: `HOPPER_80`

## Mutations

### Create/Update Template (`saveTemplate`)
Creates a new template or updates an existing one if `id` is provided.

```graphql
mutation saveTemplate($input: TemplateInput!) {
  saveTemplate(input: $input) {
    id
    name
    imageName
    containerDiskInGb
    dockerArgs
    env {
      key
      value
    }
  }
}
```

**Input Fields (`TemplateInput`):**
- `name` (String!): Template name.
- `imageName` (String!): Docker image (e.g., `runpod/serverless-python`).
- `containerDiskInGb` (Int): Disk size (default: 10).
- `dockerArgs` (String): Docker CMD.
- `env` ([EnvironmentVariableInput!]): List of `{key, value}`.
- `isServerless` (Boolean): Set to `true` for serverless templates (if applicable, or inferred).

### Create/Update Endpoint (`saveEndpoint`)
Creates a new endpoint or updates if `id` is provided.

```graphql
mutation saveEndpoint($input: EndpointInput!) {
  saveEndpoint(input: $input) {
    id
    name
    templateId
    gpuIds
    workersMin
    workersMax
    idleTimeout
  }
}
```

**Input Fields (`EndpointInput`):**
- `name` (String!): Endpoint name.
- `templateId` (String!): ID of the template to use.
- `gpuIds` (String!): GPU Type ID (e.g., "AMPERE_24").
- `workersMin` (Int): Min workers (0 for true serverless).
- `workersMax` (Int): Max concurrent workers.
- `idleTimeout` (Int): Seconds to wait before scaling down.
- `locations` (String): Region code (e.g. "US", "EU").

## Queries

### Get User Templates (`myself`)
Used to check for existing templates.

```graphql
query {
  myself {
    templates {
      id
      name
    }
  }
}
```

### Get Endpoints (`myself`)
Used to check for existing endpoints.

```graphql
query {
  myself {
    endpoints {
      id
      name
    }
  }
}
```
