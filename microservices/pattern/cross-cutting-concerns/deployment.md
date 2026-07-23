# Explain different Deployment Patterns.

Now I have solid grounding. Note: the book (Chapter 12) organizes these under **four** main patterns (Language-specific packaging, Service as VM, Service as Container, Serverless), while your list uses the **microservices.io site's** finer-grained taxonomy (which splits "container/VM" by single- vs. multi-instance-per-host, and adds "Service deployment platform" as its own pattern). I'll map each of your six to what the book actually says, and flag where the site's naming is more granular than the book's.

## 1. Multiple service instances per host
**Definition:** Run several service instances on one physical/virtual machine, sharing its OS.
**Book's coverage:** This is exactly what the book calls **Language-specific packaging format** (Section 12.1) when applied with multiple JVMs (or multiple services in one Tomcat) on a single machine — e.g., FTGO's Restaurant Service and other services running as separate JVM processes on the same box.
**Trade-off:**
- ✅ Fast deployment (just copy + start, few bytes over the network) and efficient resource use (OS/runtime overhead shared)
- ❌ No isolation — a misbehaving instance can degrade its neighbors; no encapsulation of the tech stack (ops must know every service's exact runtime requirements); manually deciding instance placement is hard
**Example:** Multiple Tomcat/JVM processes running different FTGO services on the same EC2 host.

## 2. Service instance per host
**Definition:** Each service instance gets its own dedicated machine.
**Book's coverage:** The book doesn't treat this as a separate named pattern — it's the "one extreme" of Language-specific packaging (opposite of #1), inheriting the same core drawbacks (no tech-stack encapsulation) but at least removing the "shared machine" isolation problem, at the cost of very poor resource utilization (a whole machine per instance).
**Trade-off:** Same benefits/drawbacks as #1, but trades resource efficiency for a bit more isolation — still no OS-level sandboxing between what's running.
**Example:** Running Restaurant Service's JAR directly on a dedicated EC2 host, one host per instance.

## 3. Service instance per VM
**Definition:** Package the service — code + runtime + dependencies — as a full VM image (e.g., an AWS AMI); each instance is a VM.
**Book's coverage:** **Service as a Virtual Machine pattern** (Section 12.2).
**Trade-off:**
- ✅ VM image **encapsulates the entire tech stack** as a black box, deployable anywhere unmodified; **full isolation** (fixed CPU/memory, can't steal from neighbors); leverages mature cloud infra (load balancing, autoscaling)
- ❌ Inefficient resource use (each instance carries a full OS); **slow deployments** (building/booting a VM image takes minutes — lots of data to move); you're still responsible for **patching the OS/runtime**
**Example:** Building an Amazon Machine Image (AMI) for Restaurant Service using **Packer**, then running it as autoscaled EC2 instances behind an Elastic Load Balancer. (The book also mentions **AWS Elastic Beanstalk** as an easier way to get this without manually building AMIs.)

## 4. Service instance per Container
**Definition:** Package the service as a container image (a lightweight OS-level virtualization unit); each instance is a container.
**Book's coverage:** **Service as a Container pattern** (Section 12.3), demonstrated with **Docker** + **Kubernetes**.
**Trade-off:**
- ✅ Most of a VM's benefits (encapsulation, isolation via sandboxing, resource limits enforceable by the container runtime) but **far more lightweight and fast** — Docker's layered filesystem means only the changed layers need transferring
- ❌ You're still responsible for the "undifferentiated heavy lifting" of administering container images and patching the OS/runtime, unless using a hosted solution (e.g., Google Container Engine, AWS ECS); a single `docker run` on one machine isn't reliable for production — needs an orchestrator
**Example:** The book's own Restaurant Service `Dockerfile` — a minimal `openjdk:8u171-jre-alpine` base image, `COPY`s the executable JAR, configures a `HEALTHCHECK` hitting `/actuator/health` every 5s. Built with `docker build`, tagged, and pushed to a registry; deployed reliably at scale via **Kubernetes**, a "Docker orchestration framework" that pools machines into one resource pool and keeps the desired instance count running even through crashes.

## 5. Serverless deployment
**Definition:** Deploy a service (as a "function") to a fully managed platform that handles all provisioning, scaling, and system administration for you.
**Book's coverage:** **Serverless deployment pattern** (Section 12.5), demonstrated with **AWS Lambda**.
**Trade-off:**
- ✅ Eliminates system administration entirely — no OS/runtime patching, no pre-provisioning of machines/containers; billed per-request based on execution time and memory; tightly integrated with other AWS services (S3, DynamoDB, Kinesis) as event triggers
- ❌ (Book notes it has real limitations, without fully detailing them in this excerpt) — different programming model required (must implement `RequestHandler<I,O>`), cold-start latency, execution time/resource limits
**Example:** A Java Lambda implementing `RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent>`, packaged as a ZIP/JAR, invoked either via an AWS API Gateway (HTTP), an AWS service event (e.g., S3 object created), a scheduled cron-like trigger, or a direct web service call.

## 6. Service deployment platform
**Definition (per the site's phrasing you gave):** A highly automated deployment platform that exposes services as an abstraction — you describe *what* to deploy, and the platform handles *how*.
**Book's coverage:** The book doesn't name this as its own separate numbered pattern the way the site does — but this is essentially **what Kubernetes and AWS Lambda both already are**, described functionally rather than by a distinct name. The book explicitly requires any production environment to implement four capabilities that match this description:
- **Service management interface** — a REST API for creating/updating/configuring services
- **Runtime service management** — keeps the desired instance count running, restarting on crash
- **Monitoring** — surfaces logs/metrics, alerts on problems
- **Request routing** — routes incoming requests to the right service instances

**Trade-off:** This is presented less as "yet another option to weigh" and more as **the necessary underlying capability** any of patterns #3–#5 need at scale — you can't reliably run "tens or hundreds of services" without one, per the book's own framing.
**Example:** Kubernetes (Section 12.4) is the book's primary worked example — it turns a set of machines into a single pool of resources, keeps instance counts correct, and integrates with a service mesh (Istio) for advanced routing (e.g., the 95%/5% v1/v2 traffic-split rule shown for canary releases). AWS Lambda + API Gateway is the book's other example of a fully managed deployment platform.

**Summary of the mapping:** the book's own four patterns (#1/#2 → Language-specific packaging, #3 → Service as VM, #4 → Service as Container, #5 → Serverless) roughly cover the site's six, with #6 ("Service deployment platform") described in the book as a *required capability* underlying #3–#5 at production scale, rather than a separately chosen alternative.

*Citation: Chapter 12, Sections 12.1–12.5, pp. 384–418.*