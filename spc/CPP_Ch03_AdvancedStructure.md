# C++ Programming — Chapter 3: Advanced Structure (Record)

> The slides show *how to type* a struct but skip what it is in memory, why `strcpy` is needed, why `student = newStudent` works when `student.firstName = newStudent.firstName` does not, and they contain code that will not compile (missing `;`, a `deprtID` typo, a string put into a `char`). This note fixes those and solves all three exercises. Everything was compiled and run with g++ 13.

## 0. One-sentence overview

A **struct** bundles related values of *different* types under one name; you can then put **arrays inside structs**, **structs inside arrays**, and **structs inside structs**.

| Section | Slides | Key idea |
|---|---|---|
| 1. Struct basics | 2–11 | define, declare, `.` access, copy, I/O |
| 2. Array in struct | 12–15 | `intList.listCode[i]` |
| 3. Struct in array | 16–19 | `employee[i].member` |
| 4. Struct in struct | 20–24 | `newEmployee.name.first` |

---

## 1. Struct basics

**Analogy:** a **student record card** with labelled boxes (name, grade, GPA). An *array* is a row of identical boxes; a *struct* is one card with different kinds of boxes.

```cpp
struct studentType {          // this is only the TEMPLATE (a new type); no memory yet
    char   firstName[10];
    char   lastName[10];
    char   courseGrade;
    int    testScore;
    int    programmingScore;
    double GPA;
};                            // <-- the semicolon is REQUIRED

studentType newStudent, student;   // now two variables exist
```

⚠️ **Missing semicolon.** Slides 20–21 end several structs with `}` and no `;`. That is a compile error: `expected ';' after struct definition`.

You reach a member with the **dot operator**: `newStudent.testScore = 100;`

### 1.1 Setting a text member (slides 7–8)

A `char` array **cannot be assigned with `=`**:

```
newStudent.firstName = "Dennis";
error: incompatible types in assignment of 'const char [7]' to 'char [10]'
```

Use `strcpy(destination, source)` — and it needs `#include <cstring>`. Without it g++ says `'strcpy' was not declared`. (The slide's `"Dennis'` with mismatched quotes is a typo.)

**Easier alternative:** declare the member as `string firstName;` (needs `<string>`). Then `s.firstName = "Dennis";` works and there is no size limit. The exercises on slides 15, 19 and 24 say "string type" for that reason.

### 1.2 The danger of `char name[10]` (slide 4)

`char firstName[10]` holds at most **9 characters + the end marker `'\0'`**. `strcpy` does **not** check length. Verified: with a 10-byte `firstName` followed by an `int score` (set to 77), `strcpy(s.firstName, "ChristopherLee")` (14 chars) **overwrote `score`**, which afterwards printed `25957`. This "writing past the end of a buffer" is a *buffer overflow*, a classic cause of crashes and security holes. With `string` it cannot happen.

### 1.3 Copying a whole struct (slides 9–10)

```cpp
studentType student = newStudent;     // copies EVERY member
```

Verified: after the copy I changed `newStudent.firstName` to `"Changed"`; `student.firstName` stayed `Lily`. So the copy is a full, independent duplicate **including the char arrays inside**.

⚠️ **Slide 10 misleads.** It says the assignment is "same as" writing `student.firstName = newStudent.firstName;` and so on. But slide 7 just told you that assignment is illegal for a char array. Those expanded lines would **not compile** for `firstName`/`lastName`. The truth: whole-struct `=` copies *memory member by member*, arrays included, even though `=` on a lone array is not allowed. (For non-array members the expanded lines are fine.)

### 1.4 Input / output and comparing (slide 11)

You must read and write **one member at a time**. The same limit applies to comparing: `if (x == y)` on two structs gives `error: no match for 'operator=='`, and `cout << x` fails too. Compare member by member.

⚠️ `cin >> newStudent.firstName;` into a `char[10]` has the same overflow risk as `strcpy`. `string` is safer.

*Extra (not in slides):* `sizeof(studentType)` was **40**, although the members add up to 10+10+1+4+4+8 = 37. The compiler inserts unused **padding** bytes so members sit at convenient addresses. Don't assume a struct's size is the sum of its members.

---

## 2. Arrays in structs (slides 12–15)

```cpp
struct listType {
    int listCode[1000];     // array member
    int listLength;
};
listType intList;
```

```
intList
 ├─ listCode : [0][1][2] ... [999]
 └─ listLength
```

Read the access **left to right**: `intList.listCode[10]` = "in `intList`, take `listCode`, then element 10" (the **11th** value).

| Statement | Meaning |
|---|---|
| `intList.listLength = 0;` | set the length member |
| `intList.listCode[0] = 12;` | first array element |
| `intList.listCode[1] += 5;` | add 5 to the 2nd element |
| `cin >> intList.listCode[i]` (in a loop) | read all 1000 |

**Why bother?** Keeping the array and its *length* in one struct means they travel together (e.g. into a function).

### Exercise (slide 15) — solution

```cpp
struct Student { string name; int year; float marks[5]; };
int main(){
    Student s;
    getline(cin, s.name);                    // getline so names with spaces work
    cin >> s.year;
    float total = 0;
    for (int i = 0; i < 5; i++) { cin >> s.marks[i]; total += s.marks[i]; }
    cout << s.name << " (Year " << s.year << ")  total=" << total
         << "  average=" << total / 5 << "\n";
}
```

Input `Aisha Rahman / 2 / 80 70.5 90 65 84.5` → `total=390  average=78`.

---

## 3. Structs in arrays (slides 16–19)

One array where **each element is a whole record**: `employeeType employee[50];`

```
employee: [0][1][2] ... [49]      each box holds firstName, lastName, personID, ...
```

Write it as `array[index].member`:

| Statement (slide 18) | Meaning |
|---|---|
| `employee[19].monthlySalary += 1200;` | **20th** employee (index 19) |
| `employee[49].yearToDatePaid = 84500;` | last employee |
| `cout << employee[35].firstName[4];` | 5th letter of the 36th employee's first name |

⚠️ **Slide 16 vs 18 mismatch.** Slide 16 declares `char deprtID;` (typo, and only **one** character), but slide 18 writes `strcpy(employee[0].deptID, "IT999");`. Compiled as printed: `'struct employeeType' has no member named 'deptID'; did you mean 'deprtID'?` Even after fixing the spelling, you cannot `strcpy` a 5-letter code into a single `char`. Slide 21 declares it correctly as `char deptID[10];`.

### Exercise (slide 19) — solution

```cpp
struct Employee { int empID; string name; int daysPresent; };
int main(){
    const int N = 3, WORKDAYS = 24;
    Employee Employees[N];
    for (int i = 0; i < N; i++)
        cin >> Employees[i].empID >> Employees[i].name >> Employees[i].daysPresent;
    for (int i = 0; i < N; i++)
        cout << Employees[i].empID << " " << Employees[i].name << " "
             << Employees[i].daysPresent << "/" << WORKDAYS << " = "
             << 100.0 * Employees[i].daysPresent / WORKDAYS << "%\n";
}
```

Input `101 Amy 24`, `102 Bob 18`, `103 Cat 21` → `100%`, `75%`, `87.5%`.

**Why `100.0 *`:** `18 / 24` in integers is 0. Multiplying by `100.0` first forces decimal arithmetic.

---

## 4. Structs in structs (slides 20–24)

Splitting big records into sub-records keeps each piece reusable (one `dateType` for both `hireDate` and `quitDate`).

```cpp
struct nameType { char first[10]; char middle[10]; char last[10]; };   // note the ';'
struct dateType { int month, day, year; };
struct employeeType {            // shortened; slide 21 also has addressType address,
    nameType name;               // contactType contact, deptID ... built the same way
    char empID[10];
    dateType hireDate, quitDate;
    double salary;
};
employeeType newEmployee;
```

**Rule:** a struct used as a member must be **defined before** the struct that contains it.

Access by chaining dots, **outermost first**:

```cpp
strcpy(newEmployee.name.first, "John");   // newEmployee -> name -> first
newEmployee.address.zip = 53300;
cin >> newEmployee.hireDate.month;
```

### Exercise (slide 24) — solution

⚠️ The slide says `ownerIC` is an **integer**. A Malaysian IC has 12 digits, which does not fit in a 32-bit `int` (max 2 147 483 647), and an integer **drops leading zeros**: I tested `010203101234` and it printed `10203101234`. An identifier is not a quantity; store it as a `string` (or at least `long long` if the exercise insists on a number).

```cpp
struct Car   { string brand, model; int yearMade; };
struct Owner { string name; long long ownerIC; Car car; };    // Car defined first
int main(){
    Owner owner[3];
    for (int i = 0; i < 3; i++) {
        cin >> owner[i].name >> owner[i].ownerIC
            >> owner[i].car.brand >> owner[i].car.model >> owner[i].car.yearMade;
    }
    for (int i = 0; i < 3; i++)
        cout << owner[i].name << " (IC " << owner[i].ownerIC << ") owns a "
             << owner[i].car.yearMade << " " << owner[i].car.brand << " "
             << owner[i].car.model << "\n";
}
```

Sample output: `Ali (IC 990101015555) owns a 2021 Proton X70`. (Note the second owner's IC `010203101234` printed without its leading zero; use `string` to keep it.)

---

## ⚠️ Where the slides mislead

| Slide | Slide says | What is true |
|---|---|---|
| 10 | Struct `=` is "same as" copying each member with `=` | Fine for numbers; illegal for char arrays. Struct `=` copies arrays anyway. |
| 16 vs 18 | `char deprtID;` then `strcpy(...deptID, "IT999")` | Typo, and one `char` can't hold a string. |
| 20–21 | structs closed with `}` | Missing `;` → compile error. |
| 7 | `firstName = "Dennis';` | Mismatched quotes (typo). |
| 4 | `char firstName[10]` | Holds only 9 characters. |
| 24 | `ownerIC` is an integer | Too big for `int`; loses leading zeros. |
| 7–8, 18 | `strcpy` used with no `#include <cstring>` | Needs the header. |

**Exam strategy:** if asked "why can't you write `student.firstName = "x"`?", answer as the slide does: a char array cannot be assigned directly, use `strcpy`.

## Cheat sheet

| Task | Code |
|---|---|
| define type | `struct T { int a; double b; };` **(semicolon!)** |
| declare | `T x;   T arr[50];` |
| member | `x.a` |
| member of array element | `arr[i].a` |
| array inside struct | `x.list[i]` |
| struct inside struct | `x.inner.a` (outermost first) |
| copy whole struct | `y = x;` (copies arrays too) |
| compare / print struct | member by member — `==` and `<<` don't work |
| set a `char[]` member | `strcpy(x.s, "text");` + `<cstring>` (or use `string`) |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** Given `studentType student, newStudent;` (with `char firstName[10]` inside), after `student = newStudent;` then changing `newStudent.firstName`, what is `student.firstName`?
(a) also changed (b) unchanged (c) garbage (d) compile error

**A2.** Which line compiles, with `char name[10]` a member of `s`?
(a) `s.name = "Amy";` (b) `strcpy(s.name, "Amy");` (c) `s.name[] = "Amy";` (d) `s = "Amy";`

**A3.** Which expression is the 5th letter of the first name of the 36th employee in `employeeType employee[50]`?
(a) `employee[36].firstName[5]` (b) `employee[35].firstName[4]` (c) `employee[35][4].firstName` (d) `employee.firstName[35][4]`

**A4.** A struct definition must end with
(a) `}` (b) `};` (c) `)` (d) nothing

**A5.** Which header is needed for `strcpy`?
(a) `<string>` (b) `<cstring>` (c) `<cstdlib>` (d) `<sstream>`

### B. Short answer

**B1.** Explain why `if (x == y)` is illegal for two struct variables and how you would compare two students.
**B2.** Slide 10 says `student = newStudent;` is "same as" assigning each member. Explain what is misleading about this.
**B3.** Give one declaration for (i) an array inside a struct, (ii) a struct inside an array, (iii) a struct inside a struct.

### C. Calculation / trace

**C1.** `struct Item { string name; int qty; double price; };` with `Item items[3] = {{"pen",10,1.5},{"book",2,12.9},{"bag",1,45.0}};` Find the total value Σ qty × price and the name of the item with the highest `price`.
**C2.** `struct P { int a[3]; }; P x = {{1,2,3}}; P y = x; y.a[0] = 99;` What are `x.a[0]` and `y.a[0]`?
**C3.** Three employees have `daysPresent` 24, 18 and 21 out of 24 working days. Give each attendance percentage.

### D. Thinking

**D1.** `char firstName[10]` followed by `strcpy(s.firstName, userInput)` — describe the risk and two ways to remove it.
**D2.** You must store 100 books (title, author, price) and find the cheapest. Which composition of arrays/structs do you use and how do you find the cheapest?

---

### Answers

**A1 → (b) unchanged.** Struct assignment makes an independent copy, arrays included (verified: `Lily` stayed while the original became `Changed`).

**A2 → (b).** Char arrays can't be assigned with `=`; use `strcpy`.

**A3 → (b).** 36th → index 35; 5th letter → index 4.

**A4 → (b) `};`.** Without the `;` you get `expected ';' after struct definition`.

**A5 → (b) `<cstring>`.** (`<string>` is for the `string` class.)

**B1.** A struct has no built-in `==`; the compiler doesn't know what "equal" means for it (`no match for 'operator=='`). Compare the members that matter, e.g. `x.id == y.id && x.name == y.name`.

**B2.** It suggests each member is copied by an ordinary `=` statement. That works for `int`/`double`, but the char-array members can't be assigned with `=` (slide 7 says so). Whole-struct `=` copies the raw contents, so arrays *are* copied even though the expanded lines would not compile.

**B3.** (i) `struct listType { int listCode[1000]; int listLength; };` (ii) `employeeType employee[50];` (iii) `struct employeeType { nameType name; … };` where `nameType` was defined earlier.

**C1.** Total = 10×1.5 + 2×12.9 + 1×45.0 = 15 + 25.8 + 45 = **85.8**; highest price = **bag** (45.0). Verified.

**C2.** `x.a[0]` = **1**, `y.a[0]` = **99**. The array is copied, so `y` is independent. Verified.

**C3.** 24/24 = **100%**, 18/24 = **75%**, 21/24 = **87.5%**. Use `100.0 * days / 24` (integer division would give 0 for 18/24). Verified.

**D1.** `strcpy` doesn't check length. Input of 10 or more characters writes past the end of `firstName` and corrupts the next member or memory (verified: it changed `score` from 77 to 25957). Fixes: (1) use `string firstName;`; (2) if you must use `char[]`, use a bounded copy, e.g. `strncpy` with the last byte set to `'\0'`, or `cin >> setw(10) >> s.firstName`.

**D2.** `struct Book { string title; string author; double price; }; Book shelf[100];` Set `cheapest = 0`; for `i = 1 … 99`, if `shelf[i].price < shelf[cheapest].price` then `cheapest = i`. (Same pattern as "find the largest" from Chapter 1; verified on 4 sample books, it selected price 25.0.)

---

## Links to other chapters

- **Ch 1:** arrays and the "find the largest" pattern; here the array elements are structs.
- **Ch 6:** passing a struct to a function by value, by address, or by reference; returning a struct.
- **Ch 8:** `typedef struct { … } Passenger;` and `enum` are other user-defined types.
- **Ch 11:** the global-struct example (`Employee emp;`) is used to explain *common coupling*.
