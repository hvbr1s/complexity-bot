async def prepare_evm_prompt_fv(file_path, code_lines, code_to_comment_ratio, solidity_contract, protocol):
   try:
      EVM_ANALYZER = f''' 
Your task is to analyze a Solidity (.sol) file intended for building a smart contract for the {protocol} project on the Ethereum blockchain and provide a complexity score to guide its formal verification.

Here is the Solidity file to analyze:

<solidity_file>
{solidity_contract}
</solidity_file>

Here is the metadata for the file:
- Project name: {protocol}
- File name: {file_path}
- Number of lines of code: {code_lines}
- Percentage of commented lines of code: {code_to_comment_ratio}%

Analyze the potential complexity of the code based on the following criteria, think step-by-step:

<thinking>
1. Categorize the program size as:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large
     
2. Locate and briefly note the most complex or security-critical public functions

3. Evaluate the code's potential challenges for formal verification:
  - Higher complexity when formally verifying non-linear arithmetic due to SMT limitations
  - Implementation of non-linear mathematical operations
  - Number and length of copy-loops produced by the solidity compiler due to complex data structures

4. Assess the following Ethereum-specific complexity factors for formal verification:
  - Use of delegate calls
  - Presence of assembly code
  - Implementation of low-level calls
  - Number and complexity of state variables
  - Use of complex data structures (mappings, nested mappings, structs, byte arrays)
  - Implementation of upgradeable contracts and proxy patterns
  - Interdependencies between contracts potentially due to proxy patterns

5. Consider the number of calls to other contracts, the more calls the more complex the contract for formal verification:
   - Direct function call (example: `OtherContract(address).functionName();`)
   - Low-level call (example: `address(contractAddress).call(abi.encodeWithSignature("functionName(uint256)", arg));`)
   - Interface-based call (example: `IContractInterface(address).functionName();`)
   - Library usage (example: `LibraryName.functionName();`)
   - Delegate calls from Contract B to Contract A (example: 
      ```function delegateCallToContractA(uint256 _data) public {{
         // Perform delegate call to Contract A’s setData function
         (bool success, ) = contractAAddress.delegatecall(abi.encodeWithSignature(“setData(uint256)“, _data));
         require(success, “Delegate call failed”);
      }}```
   - Using ‘this’ for external calls within the same contract (example: `address(this)`)

6. Analyze external dependencies:
   - Number and nature of imported contracts or libraries
   - Use of established libraries (e.g., OpenZeppelin) vs custom implementations which are more challenging to audit
   - Contract constructor dependencies and general inheritance structure, the more inherited the more complex

7. Assign a complexity score from 1 to 10, where:
    1-3: Simple contract with straightforward logic and easily formally verified code.
    4-6: Moderate complexity contract with some challenge for formal verification.
    7-10: High complexity contract with delegate calls, assembly, complex state management, and non-linear mathematics that are difficult to formally verify.
</thinking>

Your response must be a JSON file with the following expected output:
{{
  "purpose": "[INSERT BRIEF DESCRIPTION OF THE PROGRAM'S PURPOSE HERE]",
  "complexity": "[SCORE AS A SINGLE NUMBER FOR EXAMPLE 5]",
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
   

async def prepare_sol_prompt_fv(file_path, code_lines, code_to_comment_ratio, rust_code, protocol):
    try:
        SOL_ANALYZER = f''' 
Your task is to analyze the following Rust-based file which is part of a larger program for the {protocol} project and intended for deployment on the Solana blockchain and provide a complexity score to guide its formal verification.
    
Here is the Rust code to analyze:
<rust_code>
{rust_code}
</rust_code>

Here is the metadata for the code:
- Project name: {protocol}
- File name: {file_path}
- Number of lines of code: {code_lines}
- Percentage of commented lines of code: {code_to_comment_ratio}%

Analyze the potential complexity of the program based on the following criteria, think step-by-step:

<thinking>
1. Categorize the program size as:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large
     
2. Evaluate the percentage of commented code, the higher the better.

3. Consider the number of entry points (e.g., 'pub fn'), the more entry points, the more complex to formally verify the program

4. Locate and briefly note the functions that could be formally verified

5. Evaluate the program's potential challenges for formal verification:
   - Look for presence of floating-point operations (f32 or f64) vs. scaled integers, the presence of floating points make formal verification extremely difficult.
   - Check for implementation of non-linear mathematical operations (e.g., 'checked_mul', 'checked_div')
   - Identify implementation of complex data structures like Merkle trees, hash tables or binary trees
   - Frequency and complexity of Cross-Program Invocations (CPI) (look for 'invoke' or 'invoke_signed' functions)

6. Assess Solana-specific complexity factors for formal verification:
   - Use of Program Derived Addresses (PDAs)
   - Implementation of complex account validation logic
   - Handling of multiple signers or complex signer validation
   - Reliance on custom libraries over established ones (e.g., SPL library)
   - Proper handling of account ownership and type checks
   - Correct implementation of rent exemption checks

7. Analyze the code's external dependencies:
   - Note the number and nature of external crates used
   - Note that the use of Borsh simplifies serializing and deserializing data structures (look for 'use borsh').
   - Note that the use of Bytemuck simplifies low-level data manipulation (look for 'use bytemuck').
   
8. Based on your analysis, assign a complexity score from 0 to 10, where:
- 0: Extremely short or simple file that is not worth formally verifying
- 1-3: Simple Solana program with straightforward and easily formally verified logic
- 4-6: Moderate complexity program with logic that is more challenging to formally verify
- 7-10: High complexity program with multiple CPIs, complex account structures, and non-linear mathematics that are difficult to formally verify
</thinking>

Your response must be a JSON file with the following structure:

<output>
{{
  "purpose": "[INSERT BRIEF DESCRIPTION OF THE PROGRAM'S PURPOSE HERE]",  
  "complexity": "[SCORE AS A SINGLE NUMBER FOR EXAMPLE 5]",
  "rationale": "[INSERT ONE-SENTENCE EXPLANATION HERE]"
}}
</output>

Do not include any additional information or explanations outside of this JSON structure. Ensure that your rationale is concise and directly relates to the assigned complexity score.
        '''
        
        return SOL_ANALYZER
     
    except Exception as e:
        print(e)
        error  = {
            "purpose": "Oops, something went wrong, I wasn't able to score that file!",
            "complexity": "0",
            "rationale": "Oops, something went wrong, I wasn't able to score that file!"
         }
        return error
