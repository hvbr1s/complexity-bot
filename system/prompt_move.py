async def prepare_move_prompt(file_path, code_lines, comment_lines, code_to_comment_ratio, move_code, protocol):
   try:
      MOVE_ANALYZER = f'''     
Your task is to analyze Move (.move) files intended for deployment on the Aptos blockchain and provide a complexity score to guide manual security audits and formal verification processes.

Here is the Move code to analyze:
<move_code>
{move_code}
</move_code>

Here is the metadata for the code:
- Project name: {protocol}
- File name: {file_path}
- Number of lines of code: {code_lines}
- Number of lines of comments: {comment_lines}
- Percentage of commented lines of code: {code_to_comment_ratio}%

Analyze the potential complexity of the program based on the following criteria, think step-by-step:

<thinking>

1. Categorize the program size as:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large
     
2. Assess the following Move and Aptos-specific complexity factors:
   - Use of generic types and type parameters
   - Implementation of resource types (structs with the `key` ability)
   - Use of abilities (copy, drop, store, key)
   - Implementation of complex data structures (vectors, tables)
   - Use of native functions and modules
   - Implementation of module upgrades (if applicable)

3. Consider the number of calls to other modules, the more calls the more complex the contract:
   - Function calls within the same module
   - Cross-module function calls
   - Use of the `use` statement for importing other modules
   - Calls to standard library functions
   - Event emission

4. Consider security-focused elements:
   - Proper access control mechanisms (use of `public`, `public(friend)`, etc.)
   - Correct implementation of resource management
   - Handling of Aptos Coin transfers and potential re-entrancy vulnerabilities

5. Analyze external dependencies:
   - Number and nature of imported modules
   - Use of established libraries vs custom implementations

6. Identify critical functions:
   - Locate and briefly note the most complex or security-critical functions

7. Evaluate the percentage of the code that is commented, the higher the percentage the better.

8. Assign a complexity score from 1 to 10, where:
    1-3: Simple contract with straightforward logic and easily formally verified code.
    4-6: Moderate complexity contract with potential security considerations.
    7-10: High complexity contract with complex resource management, generic types, and non-linear mathematics that are difficult to formally verify.
</thinking>

Your response must be a JSON file with the following structure:

<output>
{{
  "purpose": "[INSERT BRIEF DESCRIPTION OF THE PROGRAM'S PURPOSE HERE]",
  "complexity": "[INSERT SCORE HERE]",
  "rationale": "[INSERT ONE-SENTENCE EXPLANATION HERE]"
}}
</output>

Do not include any additional information or explanations outside of this JSON structure. Ensure that your rationale is concise and directly relates to the assigned complexity score.
'''
      return MOVE_ANALYZER
   
   except Exception as e:
      print(e)
      return MOVE_ANALYZER