async def prepare_go_prompt(file_path, code_lines, comment_lines, code_to_comment_ratio, go_file):
   try:
      GO_ANALYZER = f''' 
Your task is to analyze Go files intended for interaction with the Ethereum ecosystem (but not deploying smart contracts) and provide a complexity score to guide manual security audits.

Here is the Go code to analyze:

<go_code>
{go_file}
</go_code>

Analyze the provided Go code carefully, think step-by-step:

<thinking>
1. Note the following metadata:
   - File name: {file_path}
   - Number of lines of code: {code_lines}
   - Number of lines of comments: {comment_lines}
   - Percentage of commented lines of code: {code_to_comment_ratio}%

2. Categorize the file based on its size:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large   

3. Assess the following Ethereum-adjacent complexity factors:
   - Interaction with Ethereum nodes or APIs (look for packages like 'go-ethereum' or 'ethclient')
   - Implementation of cryptographic operations (e.g., key management, signing)
   - Handling of Ethereum addresses and transactions
   - Use of complex data structures like Merkle trees or patricia tries
   - Implementation of Ethereum-specific encoding (e.g., RLP, ABI)

4. Consider security-focused elements:
   - Proper handling of sensitive data (e.g., private keys)
   - Secure communication with Ethereum nodes
   - Number of entry points (e.g., exported functions)
   - Error handling and logging practices

5. Analyze external dependencies:
   - Number and nature of external packages used
   - Use of well-known Ethereum-related libraries (e.g., 'go-ethereum')
   - Use of cryptographic libraries (e.g., 'crypto', 'x/crypto')

6. Identify critical functions:
   - Locate and briefly note the most complex or security-critical functions

7. Evaluate the percentage of the code that is commented, the higher the percentage the better.

8. Finally, assign a complexity score from 1 to 10, where:
    1-3: Simple Go program with straightforward Ethereum interactions and easily verified logic.
    4-6: Moderate complexity program with potential security considerations.
    7-10: High complexity program with multiple Ethereum interactions and complex implementations.
    
</thinking>

Your response must be a JSON file with the following structure:
{{
  "complexity": "[SCORE]",
  "rationale": "[ONE SENTENCE EXPLANATION]"
}}

Do not include any additional information or explanations outside of this JSON structure. Ensure that your rationale is concise and directly relates to the assigned complexity score.
'''
      return GO_ANALYZER
   
   except Exception as e:
      print(e)
      return GO_ANALYZER