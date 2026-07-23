Good — the sidecar concept **is** covered in the book, just not as its own standalone numbered pattern. It shows up in **Chapter 12, "Deploying microservices,"** Section 12.4 ("Deploying the FTGO application with Kubernetes"), within the discussion of **Istio as a service mesh implementation**.

## Definition (the book's own wording, p. 410)
> Istio uses Envoy as a **sidecar**, a process or container that runs alongside the service instance and implements cross-cutting concerns.

So a sidecar is: a *separate* process/container, deployed **next to** your service (not inside it), that handles concerns your service code doesn't have to.

## How it works, per the book's Istio example
- Istio's architecture has a **control plane** (the Pilot and the Mixer) and a **data plane** — the data plane consists of **Envoy proxies, one per service instance**.
- **Envoy** is a high-performance proxy supporting TCP, HTTP/HTTPS, and even higher-level protocols like MongoDB, Redis, and DynamoDB — plus features like circuit breakers, rate limiting, automatic retries, and TLS-secured inter-service communication.
- **On Kubernetes specifically:** the Envoy proxy runs as a **separate container inside the same Pod** as the service — that's the sidecar. (In non-Kubernetes environments without the "pod" concept, Envoy instead runs in the same container as the service.)
- **All traffic in and out of the service flows through its sidecar.** So a direct Service→Service call actually becomes: *Service → Source Envoy → Destination Envoy → Service*. Every hop is intercepted and routed according to rules the control plane (Pilot) pushes down to it.
- The **Pilot** extracts info about deployed services from the infrastructure (e.g., Kubernetes services/pods) and configures each Envoy sidecar's routing rules; the **Mixer** collects telemetry from the sidecars and enforces policies like quotas.

## How the sidecar gets attached to your service (deployment mechanics)
The book gives two ways to inject the Envoy sidecar into a service's Kubernetes Pod:
1. **Manual sidecar injection** — run `istioctl kube-inject -f <deployment.yml> | kubectl apply -f -`, which reads your existing Kubernetes YAML and outputs a modified version with the Envoy sidecar added.
2. **Automatic sidecar injection** — enable a feature so that a normal `kubectl apply` automatically triggers Istio to modify the pod definition and inject the sidecar — no manual step needed.

## Why this matters — the payoff
Because the sidecar intercepts *all* traffic, your service code stays completely unaware of circuit breaking, retries, TLS, distributed tracing, and traffic routing — those concerns move **out of your application code and the microservice chassis, into the sidecar**. This is exactly the point the book made earlier (Chapter 11, service mesh discussion): a service mesh dramatically shrinks what the microservice chassis needs to do, and the sidecar is the concrete mechanism that makes that possible.

## How this ties to what we've covered
- It's the deployment-level realization of the **Service Mesh** concept we discussed — Istio *is* one of the three service mesh implementations the book named (Istio, Linkerd, Conduit), and the sidecar is literally how Istio attaches itself to each service instance.
- The Pilot/Mixer + Envoy setup also directly enables **Distributed Tracing** and **Application Metrics** (Chapter 11 patterns) to work without your service code doing anything extra — traffic passing through the sidecar is exactly where trace spans and metrics get captured.
- The sidecar's traffic-routing capability is also what enables **separating deployment from release** — running two versions of a service (`v1`, `v2`) simultaneously and routing only test users to the new one, which the book demonstrates right after introducing sidecars.

*Citation: Chapter 12, Section 12.4.4 ("Understanding Istio"), pp. 407–410.*