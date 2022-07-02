# Transactions
Practice evaluating the properties of transactions schedules and writing transaction statements.

 ## Overview of files
 ### [part1.txt](art1.txt)
 Two questions and answers about scheduling transactions.

 ### [part2.pdf](part2.pdf)
 Discusses why the three transactions and schedule in the box all the way to the left are not conflict serializable.

  ### [part3.pdf](part3.pdf)
  a. Adds locks to the schedule in [part 2](part2.pdf). Uses a two-phase locking system to ensure a conflict-serializable schedule for the transactions. Uses the notation L(A) to indicate that a transaction acquires the lock on element A and U(A) to indicate that the transaction releases its lock.

  b. Discussion of why we need strict 2PL when 2PL ensures conflict serializability.
