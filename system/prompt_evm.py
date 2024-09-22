async def prepare_evm_prompt(file_path, code_lines, comment_lines, code_to_comment_ratio, solidity_contract, protocol):
   try:
      EVM_ANALYZER = f''' 
Your task is to analyze a Solidity (.sol) file intended for deployment on the Ethereum blockchain and provide a complexity score to guide manual security audits and formal verification processes.

Here is the Ethereum smart contract to analyze:

<solidity_contract>
{solidity_contract}
</solidity_contract>

Analyze the provided Solidity contract carefully, make sure to think step-by-step:

<thinking>
1. Code metadata:
   - Project name: {protocol}
   - File name: {file_path}
   - Number of lines of code: {code_lines}
   - Number of lines of comments: {comment_lines}
   - Percentage of commented lines of code: {code_to_comment_ratio}%

2. Analyze the potential complexity of the Ethereum smart contract based on:
   - Number of lines of code
   - Actual code content and structure
   - Contract size categorization:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large

3. IMPORTANTLY, evaluate the contract's potential challenges for formal verification, considering:
  - Higher complexity when formally verifying non-linear arithmetic due to SMT limitations
  - Implementation of non-linear mathematical operations
  - Number and length of copy-loops produced by the solidity compiler due to complex data structures

4. Assess the following Ethereum-specific complexity factors:
  - Use of delegate calls
  - Presence of assembly code
  - Implementation of low-level calls
  - Number and complexity of state variables
  - Use of complex data structures (mappings, nested mappings, structs, byte arrays)
  - Implementation of upgradeable contracts and proxy patterns
  - Interdependencies between contracts potentially due to proxy patterns

5. Consider the number of calls to other contracts, the more calls the more complex the contract:
   - Direct function call (example: `OtherContract(address).functionName();`)
   - Low-level call (example: `address(contractAddress).call(abi.encodeWithSignature("functionName(uint256)", arg));`)
   - Interface-based call (example: `IContractInterface(address).functionName();`)
   - Library usage (example: `LibraryName.functionName();`)
   - Delegate calls from Contract B to Contract A (example: ```function delegateCallToContractA(uint256 _data) public {{
        // Perform delegate call to Contract A’s setData function
        (bool success, ) = contractAAddress.delegatecall(abi.encodeWithSignature(“setData(uint256)“, _data));
        require(success, “Delegate call failed”);
    }}`
   - Using ‘this’ for external calls within the same contract (example: `address(this)`)

6. Consider security-focused elements:
   - Proper access control mechanisms
   - Correct implementation of the checks-effects-interactions pattern
   - Handling of ETH transfers and potential re-entrancy vulnerabilities

7. Analyze external dependencies:
   - Number and nature of imported contracts or libraries
   - Use of established libraries (e.g., OpenZeppelin) vs custom implementations
   - Contract constructor dependencies and general inheritance structure, the more inherited the more complex

8. Identify critical functions:
   - Locate and briefly note the most complex or security-critical functions

9. Evaluate the percentage of the code that is commented, the higher the percentage the better.

10. Assign a complexity score from 1 to 10, where:
    1-3: Simple contract with straightforward logic and easily formally verified code.
    4-6: Moderate complexity contract with potential security considerations.
    7-10: High complexity contract with delegate calls, assembly, complex state management, and non-linear mathematics that are difficult to formally verify.
</thinking>

Your response must be a JSON file with the following structure:
{{
  "purpose": "[INSERT BRIEF DESCRIPTION OF THE PROGRAM'S PURPOSE HERE]",
  "complexity": "[SCORE]",
  "rationale": "[ONE SENTENCE EXPLANATION]"
}}

Do not include any additional information or explanations outside of this JSON structure. Ensure that your rationale is concise and directly relates to the assigned complexity score.
'''
      return EVM_ANALYZER
   
   except Exception as e:
      print(e)
      error  = {
            "purpose": "Oops, something went wrong, I wasn't able to score that file!",
            "complexity": "0",
            "rationale": "Oops, something went wrong, I wasn't able to score that file!"
         }
      return error