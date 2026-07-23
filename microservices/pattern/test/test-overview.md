Definitions:

Functional Test - Behaviour
- Component Test - One Iolated Microservice Test 
* Unit Test - Isolated Class, Attribute & Method Test
* Integration Test - Isolated Server + DB Test  
* E2E Test - Isolated UI/UX + Server + DB Test
- Contract Test - Interface Contract Test
Non Functional Test - Non Behaviour
- Short and Long Term Performance Test (Process & Memory) - How Fast and Stable Software is 
- Load Test - Normal Traffic Load Test
- Stress Test - Extra Traffic Load Test
- Penetration Test - Security Test
Test Process 
- Smoke Test - Superficial Test of Most Critical Aspect 
- Sanity Test - In-Depth TEst of even Least Critical Aspect
- User Acceptance Test - Product/Business/User Level Test 
Test Doubles:
- Dummy
- Stub
- Spy
- Mock
- Fake

Infographics:

Double Input
|
V
Method (Dummy (Unused Ones), Stub (Used Ones), Spy (Stub that stores the Status of the Test Target))
|
V
Double Input

Expect(Test Target Method Value that records the Status, Accepted Output)

Mock is a Stub that has Expect() within it

Fake is Stub with some implementation like a in memory database