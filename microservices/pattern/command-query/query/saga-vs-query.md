Good question — these solve two completely different problems, even though both deal with data spread across services. Here's the distinction the book draws (Chapters 4 and 7):

| | **Saga** | **API Composition** |
|---|---|---|
| **Chapter** | 4 – Managing transactions with sagas | 7 – Implementing queries |
| **Type of operation** | **Writes/commands** — updating data across multiple services | **Reads/queries** — retrieving data across multiple services |
| **Problem it solves** | How to maintain data consistency when a business operation (e.g., `createOrder()`) must update several services' databases, without distributed transactions | How to answer a query (e.g., `findOrder()`) when the needed data is scattered across several services' databases |
| **How it works** | A **sequence of local transactions**, each committing independently, coordinated over time via asynchronous messaging (choreography or orchestration) | A single component (**API composer**) calls each relevant service's query API **at the same time/on demand** and merges the responses |
| **Timing** | Happens over a sequence of steps — later steps depend on earlier ones completing; can take time and may span multiple messages | Happens essentially at once — the composer fires off calls and joins the results synchronously to answer one request |
| **Failure handling** | If a later step fails, earlier steps must be explicitly undone with **compensating transactions** (no isolation, no atomic rollback) | If a provider service is slow/down, the query just fails or degrades — there's no "undo," because nothing was changed |
| **Consistency model** | Eventual consistency across services' write state | Doesn't change any data — just assembles a consistent-enough view for reading |
| **Example from the book** | `createOrder()`: Order Service → Consumer Service → Kitchen Service → Accounting Service, with compensating transactions on failure | `findOrder()`: Find Order Composer calls Order, Kitchen, Delivery, and Accounting Services and joins results by `orderId` |

**One-line summary:** Saga is about safely **writing** data consistently across services over time; API Composition is about efficiently **reading** and assembling data from multiple services for a single response.

**Where they can appear together:** in the Chapter 13 refactoring discussion, after extracting a service, the old monolith's writes often become a saga, *and* the old monolith's reads (that used to be a SQL join) often become an API composition — they're the "write-side" and "read-side" answers to the same underlying fact: data that used to live in one database now lives in several.