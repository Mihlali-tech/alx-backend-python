# 0x03. Unittests and Integration Tests

This project focuses on writing unit tests and integration tests in Python to ensure that code behaves as expected. It emphasizes test-driven development using the `unittest` module and `parameterized` library.

## 📚 Learning Objectives

- Understand and apply unit testing in Python
- Use `parameterized` to test multiple cases with one function
- Mock inputs and outputs
- Write integration tests for API calls

---

## Task 0: Parameterize a unit test

📄 **File:** `test_utils.py`

✅ In this task, we created unit tests for the function `access_nested_map()` from `utils.py`.  
✅ The tests use the `@parameterized.expand` decorator to cover multiple test cases using different map structures and key paths.

🧪 Example tested cases:
```python
access_nested_map({"a": 1}, ["a"])        # should return 1
access_nested_map({"a": {"b": 2}}, ["a", "b"])  # should return 2
