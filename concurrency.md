## Concurrency Issues

### Case 1: Read skew when selecting and updating a profile
1. Alice and Bob both have profiles for Spicify's recipe blog.
2. Alice is in the process of updating her profile.
3. Before her Profile can be committed, Bob pulls up Alice’s profile to look at her about me, but receives the profile information from before Alice updated her information. 
4. The new information is committed but now the information that Bob has does not match the latest update.

**Solution:** Read skews can be prevented with the repeatable read isolation level which would ensure consistency even with updating the database.
