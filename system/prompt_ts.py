async def prepare_ts_prompt(file_path, code_lines, comment_lines, code_to_comment_ratio, code):
   try:
      TYPESCRIPT_ANALYZER = f'''     
Your task is to analyze TypeScript files which are part of a project intended for interacting with the Ethereum blockchain and provide a complexity score to guide manual security audits.

Here is the TypeScript code to analyze:
<ts_code>
{code}
</ts_code>

Here is the metadata for the code:
- File name: {file_path}
- Number of lines of code: {code_lines}
- Number of lines of comments: {comment_lines}
- Percentage of commented lines of code: {code_to_comment_ratio}%

Analyze the potential complexity of the file based on the following criteria, think step-by-step:

<thinking>
1. Categorize the file size as:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large

2. IMPORTANTLY, evaluate the code's potential challenges for security, considering:
   - Complexity introduced by asynchronous operations and callback functions
   - Implementation of complex mathematical operations

3. Assess the following TypeScript and blockchain-specific complexity factors:
   - Use of advanced TypeScript features (generics, decorators, etc.)
   - Interaction with smart contracts (e.g., via web3.js or ethers.js)
   - Implementation of complex data structures
   - Use of asynchronous operations and promises
   - Handling of Ethereum-specific data types (big numbers, addresses)
   - Management of gas estimation and transaction handling

4. Consider the number of calls to other modules and external services, the more calls, the more complex the project:
   - Function calls within the same module
   - Cross-module function calls
   - Use of import statements for importing other modules
   - Calls to external libraries (e.g., web3.js, ethers.js)
   - Event handling and emission (e.g., listening to smart contract events)

5. Consider security-focused elements:
   - Proper handling of user inputs and avoidance of injection attacks
   - Secure management of private keys and sensitive data
   - Correct implementation of transaction signing and submission
   - Handling of Ether or token transfers and potential re-entrancy vulnerabilities
   - Mitigation of common web vulnerabilities (e.g., cross-site scripting, CSRF)

6. Analyze external dependencies:
   - Number and nature of imported modules
   - Use of established libraries (e.g., web3.js, ethers.js) vs. custom implementations
   - Potential security risks from third-party libraries

7. Identify critical functions:
   - Locate and briefly note the most complex or security-critical functions

8. Based on your analysis, assign a complexity score from 1 to 10, where:
    1-3: Simple project with straightforward logic and minimal security considerations.
    4-6: Moderate complexity project with potential security considerations.
    7-10: High complexity project with complex asynchronous operations, extensive external interactions, and advanced TypeScript features that may introduce security risks.
</thinking>

Your response must be a JSON file with the following structure:

<output>
{{
  "complexity": "[INSERT SCORE HERE]",
  "rationale": "[INSERT ONE-SENTENCE EXPLANATION HERE]"
}}
</output>

Do not include any additional information or explanations outside of this JSON structure. Ensure that your rationale is concise and directly relates to the assigned complexity score.
'''
      return TYPESCRIPT_ANALYZER
   
   except Exception as e:
      print(e)
      return TYPESCRIPT_ANALYZER