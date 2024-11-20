## Concurrency Issues

### Case 1: Read skew when selecting and updating a profile
1. Alice and Bob both have profiles for Spicify's recipe blog.
2. Alice is in the process of updating her profile.
3. Before her Profile can be committed, Bob pulls up Alice’s profile to look at her about me, but receives the profile information from before Alice updated her information. 
4. The new information is committed but now the information that Bob has does not match the latest update.

**Solution:** Read skews can be prevented with the repeatable read isolation level which would ensure consistency even with updating the database.

### Case 2: Phantom read during recipe filtering 
1. Alice filters for recipes with "vegan" ingredients and a preparation time under 30 minutes.
2. While her query is running, Bob posts a new vegan recipe that fits Alice’s filter criteria.
3. Alice does not see Bob’s recipe in her results, leading to an incomplete view of available options.

**Solution:** Use serializable isolation during filtering to ensure the dataset does not change while queries are executed. 

### Case 3: Inconsistent rating value during concurrent recipe rating
1. Alice rates a recipe with 5 stars.
2. Bob rates the same recipe with 3 stars at the same time.
3. Due to concurrent updates, the average rating is calculated using only one of their inputs, leading to an incorrect result.

**Solution:** Use row-level locking for rating updates to ensure all inputs are processed accurately.

Sequence diagrams: https://lucid.app/lucidchart/ecac2229-1b4f-4f16-b67a-21ea3e3bb87e/edit?invitationId=inv_3b7f757a-62b3-4cdd-9007-3911758475be&page=0_0#
