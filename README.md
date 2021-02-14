# This was an exercise that i did on a class Artificial Intelligence in University
---

## **Question 1 - Reflex Agent**

Η λογική είναι:
1. να αποφύγει ο pacman όλα τα ghosts
2. να μην σταματάει γιατί χάνει χρόνο άσκοπα
3. και τέλος να επιβραβεύεται με ποιο μεγάλο return αν είναι κοντά σε
φαγητό

## **Question 2 – Minimax**

Γενικά Υλοποίησης:
Έχω κατασκευάσει μία συνάρτηση μέσα στην getAction(self, gameState) με
όνομα MINMAX(gameState, agentIndex, depth) για να μπορώ να την
καλέσω μόνο μέσα από την getAction.
Επειδή δεν έχουμε μόνο ένα φάντασμα για να κάνει το για το MIN αλλά
πολλά πρέπει η σειρά να είναι pacman->ghost1->ghost2…->ghostn-
>pacman. ‘Οπου όλα τα ghosts είναι MIN, ο pacman MAX και παίζει
πρώτος.
Εκτελούμε κανονικά τον αλγόριθμο MIN (για τα ghosts) και MAX (για τον
pacman) και κάθε φορά που μπαίνουμε στην συνάρτηση ελέγχουμε να
βρούμε ποιος θα είναι ο επόμενος παίκτης, κάποιο ghost ή ο pacman. Και
για να καλεσουμε την MINMAX για τα παιδιά του απλά κάνουμε +1 στο
Index του εκτός άμα είμαστε το τελευταίο ghost θέλουμε να καλέσουμε
τον pacman με index 0.
Σχετικά με τον Minimax:
MIN: Απλά για κάθε children node καλούμε την συνάρτηση αναδρομικά
για να πάρουμε την τιμή τους [αφού στο τελευταίο επίπεδο γυρνάμε την
evaluation function] και παίρνουμε τον min των παιδιών.
MAX: Ίδιο με το MIN αλλά παίρνουμε το max των παιδιών.

## **Question 2 – AlphaBeta Pruning**

Ο αλγόριθμος είναι ίδιος με του Minimax στο question 2. Μόνο που ο AlphaBeta
είναι ποιο αποδοτικός γιατί δεν ελέγχει όλα τα Nodes.
Η συνάρτηση μας λέγεται AlphaBeta(gameState, agentIndex, depth, alpha, beta).
Και κάθε φορά που ελέγχουμε για κάθε παιδί ενός node κοιτάμε να δούμε εάν ο
parent node είχε πριν κάποιο καλύτερη επιλογή. Αν είχε σημαίνει πως δεν θα
επιλέξει οτιδήποτε και να του δώσουμε άρα ας κάνουμε prune.
Αυτό το καταφέρνουμε με τις μεταβλητές alpha, beta.
Το alpha κρατάει την μεγαλύτερη τιμή και το beta την μικρότερη.
Π.χ: Όταν είμαστε ο MIN και κοιτάμε τα παιδιά μας θα το ελέγχουμε με το alpha
που το έχει φτιάξει ο πατέρας.