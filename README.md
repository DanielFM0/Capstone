# Capstone

The syntax for a file is as follows:
- The first line of the file must be the premises you have
- The second line of the file must be the formula you want to be prove
- The following lines are your proof, with the following syntax (don't forget the dots!): line number. formula. rule with justification
To start an assumption, add ass(any_letter) as follows: line number. formula. rule with justifcation, ass(a)
with the comma as in the example. To then close an assumption, use endass(a) similarly. A correct example can be found in Proofs/DeMorgan.txt
Your text file should end with an empty line. Then, in Proofchecker_v2.py, call your proof as follow: check_proof("filename") and it will check your proof.
