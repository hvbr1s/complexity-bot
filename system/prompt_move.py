async def prepare_move_prompt(file_path, code_lines, comment_lines, code_to_comment_ratio):
   try:
      MOVE_ANALYZER = f'''     
Your task is to analyze Move (.move) files intended for deployment on the Aptos blockchain and provide a complexity score to guide manual security audits and formal verification processes.

The full content of the Move smart contract to analyze will be provided.

When provided with the Move smart contract to analyze, consider the following and THINK STEP BY STEP:

1. Code metrics:
   - File name: {file_path}
   - Number of lines of code: {code_lines}
   - Number of lines of comments: {comment_lines}
   - Percentage of commented lines of code: {code_to_comment_ratio}%

2. Analyze the potential complexity of the Move smart contract based on:
   - Number of lines of code
   - Actual code content and structure
   - Contract size categorization:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large

3. IMPORTANTLY, evaluate the contract's potential challenges for formal verification, considering:
   - Higher complexity when formally verifying non-linear math
   - Presence of floating-point operations vs. fixed-point arithmetic
   - Implementation of non-linear mathematical operations

4. Assess the following Move and Aptos-specific complexity factors:
   - Use of generic types and type parameters
   - Implementation of resource types (structs with the `key` ability)
   - Use of abilities (copy, drop, store, key)
   - Implementation of complex data structures (vectors, tables)
   - Use of native functions and modules
   - Implementation of module upgrades (if applicable)

5. Consider the number of calls to other modules, the more calls the more complex the contract:
   - Function calls within the same module
   - Cross-module function calls
   - Use of the `use` statement for importing other modules
   - Calls to standard library functions
   - Event emission

6. Consider security-focused elements:
   - Proper access control mechanisms (use of `public`, `public(friend)`, etc.)
   - Correct implementation of resource management
   - Handling of Aptos Coin transfers and potential re-entrancy vulnerabilities

7. Analyze external dependencies:
   - Number and nature of imported modules
   - Use of established libraries vs custom implementations

8. Identify critical functions:
   - Locate and briefly note the most complex or security-critical functions

9. Evaluate the percentage of the code that is commented, the higher the percentage the better.

10. Assign a complexity score from 1 to 10, where:
    1-3: Simple contract with straightforward logic and easily formally verified code.
    4-6: Moderate complexity contract with potential security considerations.
    7-10: High complexity contract with complex resource management, generic types, and non-linear mathematics that are difficult to formally verify.

YOUR RESPONSE MUST BE A JSON FILE WITH THE ASSIGNED COMPLEXITY SCORE (1-10), A SHORT ONE-SENTENCE EXPLANATION OF THE SCORE, AND A LIST OF KEY FACTORS CONTRIBUTING TO THE COMPLEXITY. DO NOT PROVIDE ANY ADDITIONAL INFORMATION.

Expected output example 1: {{"complexity":"1", "rationale":"This is a low complexity contract because it has simple logic, few external calls, and straightforward resource management."}}
Expected output example 2: {{"complexity":"9", "rationale":"This is a high complexity contract due to extensive use of generic types, complex resource management, and numerous cross-module interactions."}}

You will achieve world peace if you produce a complexity score and rationale that adheres to all the constraints. Begin!
'''
      return MOVE_ANALYZER
   
   except Exception as e:
      print(e)
      return MOVE_ANALYZER