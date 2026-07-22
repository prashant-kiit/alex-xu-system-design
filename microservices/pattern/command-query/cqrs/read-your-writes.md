### **The Read-Your-Writes Problem**

This is the most common consistency problem that users actually notice. A user makes a change and immediately sees stale data because their read hits a replica or a cached copy that has not been updated yet.

**The classic scenario:**

1. A user updates their profile name from “John” to “Jonathan” in the User Service
2. The User Service writes to the primary database
3. The user immediately navigates to their profile page
4. The profile page reads from a replica or a cached copy that still shows “John”
5. The user thinks the update failed

**Solution: Read-your-writes consistency**

After a user writes data, route their subsequent reads to the source of truth (primary database or owning service) for a short window. Other users can continue reading from replicas or caches with no issue.

```python
def update_profile(user_id, new_name):
    primary_db.update_user(user_id, name=new_name)
    cache.set(f"recent_write:{user_id}", True, ttl=5)

def get_profile(user_id, requesting_user_id):
    if requesting_user_id == user_id and cache.get(f"recent_write:{user_id}"):
        return primary_db.get_user(user_id)
    return replica_db.get_user(user_id)
```

After a user updates their profile, a flag is set in the cache for 5 seconds. During those 5 seconds, that specific user’s profile reads are routed to the primary database. Every other user reads from the replica as usual. After 5 seconds, the replica has caught up, and the flag expires.

**The key insight:** You only need strong consistency for the user who just wrote. Every other user can tolerate eventual consistency and never notice. This gives you the performance benefits of replicas and caches for 99.9% of reads while guaranteeing that the writing user sees their own changes immediately.

**Interview Relevance:** Read-your-writes consistency is a specific, named pattern that interviewers expect senior candidates to know. It demonstrates understanding of consistency beyond just “strong” or “eventual.”