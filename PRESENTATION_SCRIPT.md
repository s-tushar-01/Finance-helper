# Finance Backend System - Presentation Script

This document is your step-by-step guide on how to present this backend system to your company or technical interviewers. Follow this flow to look incredibly professional and organized.

---

## 🛠️ PRE-MEETING SETUP
1. Ensure your virtual environment is active.
2. Ensure your server is running in the background: `uvicorn app.main:app --reload`
3. Have your code editor (VS Code/Cursor) open to the project folder.
4. Open a browser tab to: `http://localhost:8000/docs` (FastAPI Swagger UI).

---

## 🗣️ STEP 1: Introduce the Architecture (5 mins)
**What to show:** Your code editor (VS Code) showing the folder structure.

**What to say:**
> "Hello everyone. The assignment was to build a robust, secure, and highly scalable Finance Backend System. Rather than throwing everything into a single file, I focused on writing production-ready code using a Clean Architecture pattern.
>
> In my project tree, you'll see I separated concerns:
> - **models:** For database structures.
> - **schemas:** Pydantic models for strict Data Validation. 
> - **services:** All business logic lives here.
> - **routes:** The controllers are completely separate from the logic.
> 
> I also used FastAPI because its asynchronous nature provides incredible throughput and it automatically generates interactive API documentation, which I'll show you now."

---

## 🗣️ STEP 2: Show the API Interface (5 mins)
**What to show:** Switch to your browser tab running `http://localhost:8000/docs`.

**What to say:**
> "Because this is a Backend API assignment, I didn't build a visual frontend. Instead, FastAPI generates this interactive OpenAPI interface. This serves as the 'front-end' for developers to understand the endpoints.
>
> You can see I've organized the application by business domain: Authentication, Users, Categories, Transactions, and Analytics. Every endpoint enforces strict REST principles."

---

## 🗣️ STEP 3: Demonstrate Security / Role-Based Access (5 mins)
**What to show:** Still on the `/docs` page.

**What to say:**
> "Security and data isolation are critical for financial data. Every request in this system enforces two rules:
> 1. A user can ONLY fetch data matching their own `user_id`. It is impossible for data leaks to occur cross-user.
> 2. Strict Role-Based Access Control (RBAC). 
>
> Let me demonstrate."

**Action:** 
1. Click the green "Authorize" button at the top right.
2. Enter `viewer@example.com` and password `password123`. Click Authorize.
3. Scroll down to `/analytics/summary` and click "Try it out" -> "Execute".
4. **Point to the screen:**
> "As you can see, the API returned a 403 Forbidden error because a 'viewer' role is strictly isolated from analytical aggregation. This proves the security layers are functioning."
5. Log out of the viewer, and authorize again using `admin@example.com` (password: `password123`).

---

## 🗣️ STEP 4: The Core Feature Demo (5 mins)
**What to show:** Executing the main logic flow via Swagger.

**Action + What to say:**
1. Execute `GET /transactions`. 
> "As the admin, I can fetch all my transactions securely. You can see the system supports dynamic filtering by amount, limits, type, and even string searches."

2. Execute `POST /transactions` to show adding a live data entry.
> "Let me show you how tightly formatted our data entry is. Here is the strict format required to add a transaction:"
> *(Copy-paste this exact JSON into the Swagger Request Body)*:
```json
{
  "category_id": 1,
  "amount": 150.75,
  "type": "expense",
  "date": "2024-05-15T14:30:00Z",
  "notes": "Weekly groceries"
}
```

3. Execute `GET /analytics/summary`.
> "Here is where the business value lies. Because we just added a $150.75 expense, this endpoint dynamically calculates the user's Total Income, Total Expenses, and strict Account Balance in real-time right out of the SQL database utilizing SQLAlchemy aggregations. No balances are hard-coded—everything is derived mathematically."

---

## 🗣️ STEP 5: The "Wow Factor" - GraphQL (2 mins)
**What to show:** Open the `/graphql` route section (or Altair / GraphQL playground if available), or just explain the route code in `app/routes/graphql.py`.

**What to say:**
> "While REST is the industry standard for CRUD interactions, analysts typically demand highly customizable data. So, I also embedded Graphene into the backend to provide a fully functional GraphQL endpoint. 
> 
> This allows analytical frontend teams to request precisely the shapes of data they want without requiring me to write hundreds of specialized REST endpoints. It's fully secured behind the same JWT Authentication layer."

---

## 🤔 Anticipated Questions & Answers

**Q: Why didn't you use MongoDB or a NoSQL database?**
> A: "Financial data is highly relational. A Transaction intrinsically belongs to a Category and a User. SQL guarantees ACID compliance (Atomicity, Consistency, Isolation, Durability) which is a strict requirement for handling money."

**Q: Why did you default to SQLite instead of Postgres?**
> A: "I used SQLAlchemy as the ORM, making the code completely database agnostic. SQLite is used for immediate local development without friction, but simply changing the `.env` file's `DATABASE_URL` instantly ports this entire system to a production PostgreSQL cluster without rewriting a single line of Python."

**Q: How do you handle errors?**
> A: "I implemented global exception handlers. This ensures that no raw stack traces ever leak to the client, preventing security vulnerabilities. Every error strictly conforms to a `{'error': 'message', 'status_code': 400}` JSON format so front-end developers always receive predictable responses."

---

## 📋 APPENDIX: EXACT DATA ENTRY FORMATS
If they ask to see how data is formatted when calling the endpoints, use these exact JSON blocks:

**1. Format to add a New Transaction (`POST /transactions`)**
```json
{
  "category_id": 1,
  "amount": 150.75,
  "type": "expense",
  "date": "2024-05-15T14:30:00Z",
  "notes": "Weekly groceries"
}
```

**2. Format to add a New Category (`POST /categories`)**
```json
{
  "name": "Groceries"
}
```

**3. Format to create a New User (`POST /users`)**
```json
{
  "email": "newuser@example.com",
  "username": "johndoe",
  "password": "strongpassword123"
}
```
