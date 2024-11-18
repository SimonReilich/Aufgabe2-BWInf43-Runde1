# Aufgabe 2 - Schwierigkeiten

# Lösungsidee

Die Abstufung der Schwierigkeiten kann man als gerichteten Graphen interpretieren. Es gibt von der Aufgabe A zur Aufgabe B genau dann eine Kante, wenn A < B laut mindestens einer Klausur.

Wenn man nun von einem zufälligen Knoten aus eine zufällige Abfolge von Schritten geht, ist es wahrscheinlich (nicht sicher, da es bei Konflikten auch Kanten in beide Richtungen geben kann), bei einer schwereren Aufgabe zu landen.

Diese Idee wird im sog. “Random-Surfer-Model” realisiert. Sei $G$ der Graph, der die oben genannte Eigenschaft erfüllt. Dann müssen wir zunächst die Adjazenzmatrix $A_G$ des Graphen berechnen. Anschließend konstruieren wir die Übergangsmatrix, indem wir die Zeilensumme der Spalten der Adjazenzmatrix berechnen und alle Einträge der entsprechenden Zeilen durch die Zeilensumme teilen (die Zeilensummen aller Zeilen der Übergangsmatrix sind 1). Nun beschreibt $P_{G \space i, j}$ die Wahrscheinlichkeit, dass der Random-Surfer in einem Schritt vom Knoten $i$ zum Knoten $j$ gelangt. ($i, j \in [n]$, wobei $n = \text{Anzahl Aufgaben}$, Umbenennung der Knoten im Prinzip beliebig, im folgenden in der Reihenfolge des Alphabets, also $A \to 1, B \to 2, C \to 3, …$)

Behauptung: für $k \in N$ ist $P_{G \space i, j}^k$ die Wahrscheinlichkeit, dass der Random-Surfer in $k$ Schritten vom Knoten $i$ zum Knoten $j$ gelangt.

### Beweis:

Sei $\phi_{i, j}^k$ die Menge aller $k$-Schritt-Pfade von $i$ nach $j$, sei $\Phi_i^k$ die menge aller $k$-Schritt-Pfade von $i$ aus. geht der Random-Surfer nun von $i$ aus einen zufälligen $k$-Schritt-Pfad, ist die Wahrscheinlichkeit, dass er am Ende zu $j$ gelangt gleich $|\phi_{i, j}^k| / |\Phi_i^k|$. 

Behauptung: für $k \in N$ ist $P_{G \space i, j}^k = |\phi_{i, j}^k| / |\Phi_i^k|$ (daraus folgt die ursprüngliche Behauptung)

Induktionsbasis: $k = 1$, $P_{G \space i, j}^1 = P_{G \space i, j} = |\phi_{i, j}^1| / |\Phi_i^1|$ folgt aus der Konstruktion von $P_G$

Induktionsschritt: Sei $k \in N$ beliebig fixiert.

Induktionsannahme: Es gilt $P_{G \space i, j}^k = |\phi_{i, j}^k| / |\Phi_i^k|$

Induktionsbehauptung: Es gilt auch $P_{G \space i, j}^{k + 1} = |\phi_{i, j}^{k + 1}| / |\Phi_i^{k + 1}|$

Induktionsbeweis: Nach Definition der Matrix-Multiplikation ist $P_{G \space i, j}^{k + 1} = (P_G^k * P_G^1)_{i, j} = \sum_{v \in [n]}(P_{G \space i, v}^k * P_{G \space v, j}^1) = \sum_{v \in [n]}(P_{G \space i, v}^k * P_{G \space v, j})$ ($n$ ist die Anzahl der Knoten von $G$). Außerdem gilt $\phi_{i, j}^{k + 1} = \biguplus_{v \in [n]} \phi_{i, v}^k \phi_{v, j}^1$ und somit auch $|\phi_{i, j}^{k + 1}| = \sum_{v \in [n]} |\phi_{i, v}^k| *  |\phi_{v, j}^1|$. Selbiges gilt auch für $\Phi_i^{k+1}$, es gilt also ${1 \over |\Phi_i^{k+1}|} = \sum_{v \in [n]} {1 \over |\Phi_i^k| * |\Phi_v^1|}$

$$
P_{G \space i, j}^{k + 1} = \underbrace{\sum_{v \in [n]}(P_{G \space i, v}^k * P_{G \space v, j}) = \sum_{v \in [n]} (|\phi_{i, v}^k|/|\Phi_i^k|) * (|\phi_{v, j}^1|/|\Phi_v^1|)}_{\text{nach Induktionsannahme und Induktionsbasis}} = \\ \sum_{v \in [n]} (|\phi_{i, v}^k|*|\phi_{v, j}^1|) / (|\Phi_i^k|*|\Phi_v^1|) = (\sum_{v \in [n]} |\phi_{i, v}^k|*|\phi_{v, j}^1|)/|\Phi_i^{k+1}| = \\ |\phi_{i, j}^{k + 1}| / |\Phi_i^{k + 1}| \space q.e.d.
$$

Berechne nun die Random-Surfer-Matrix $Q$, mit $Q = \lim_{T \to \infin}({1 \over T}\sum^{T - 1}_{k = 1}P_G^k)$. $Q_{i, j}$ ist also die Durchschnittliche Wahrscheinlichkeit, von $i$ nach $j$ zu gelangen über alle Pfadlängen. 

Als Schwierigkeitsmaß für eine Aufgabe $j$ kann man nun $\sum_{i \in [n]} Q_{i, j}$ wählen, ist die Aufgabe leicht, ist es unwahrscheinlich, bei einem zufälligen Lauf bei dieser zu Enden, ist sie schwer ist es hingegen sehr wahrscheinlich.

Diese Methode liefert zwar nicht immer das ideale Ergebnis, im Verhältnis zur Laufzeit liefert sie aber eine sehr gute Approximation.

# Umsetzung

*Die Lösungsidee wurde in Python mithilfe des Moduls numpy erstellt. Auf die genaue  Dokumentation des Einlesens wird verzichtet*

Zunächst wird aus der Eingabedatei die Adjazenzmatrix erstellt. Dabei wird zunächst eine Einheitsmatrix mit der Anzahl an Zeilen gleich der Anzahl an Spalten gleich der Anzahl an zu vergleichenden Aufgaben (Variable k) mittels `adjacency_matrix = np.identity(k)` erstellt. Es wird deshalb die Einheitsmatrix verwendet, um sicherzustellen, dass es von jedem Knoten aus mindestens einen möglichen Pfad gibt (auf jeden Fall zu sich selbst). Nun wird jede Zeile der Eingabedatei einzeln eingelesen und in eine Liste mit den Aufgaben in der passenden Reihenfolge umgewandelt (z.B. “A < B < C” → {”A”, “B”, “C”}). Dann wird mittels einer for-Schleife diese Liste durchlaufen, dabei wird in der Adjazenzmatrix zu einem Eintrag $a_{i, j}$ immer genau dann $1$ hinzugefügt (`adjacency_matrix[selected.index(tasks[j][0]), selected.index(tasks[i][0])] += 1.0`), wenn die $i$-te Aufgabe in der Liste vor der $j$-ten Aufgabe steht (da “<” transitiv ist reicht es nicht aus, das immer nur mit dem aktuellem Element und seinem Vorgänger zu tun. Es gilt: A < B und B < C → A < C).

Anschließend wird die Übergangsmatrix aus der Adjazenzmatrix mithilfe der Methode `transition_matrix(adjacency_matrix)` berechnet, ein Großteil der Funktionalität wird dabei von numpy übernommen.

Als letzter Schritt in der Matrixberechnung wird nun die Random-Surfer-Matrix erzeugt, dazu muss man eine Anzahl an Schritten `steps` angeben ($Q$ ist über den Grenzwert definiert, dieser ist aber nicht exakt berechenbar. `steps = 500` ist aber mehr als ausreichend). Die Methode berechnet $\sum_0^{steps}({1 \over \text{steps} + 1} * P^{\text{steps}})$.

Durch `result = matr.sum(0)` wird nun die Spaltensumme jeder einzelnen Spalte der Random-Surfer-Matrix berechnet. Dabei ist die Reihenfolge der Einträge dieselbe wie die der zu ordnenden Aufgaben am Ende der Eingabedatei (deshalb benötigt `evaluate(difficulties, mode, fn)` nochmals den Dateinamen). Wir gehen die Liste mehrmals durch und finden immer das minimale Element, geben die korrespondierende Aufgabe auf der Konsole aus und setzen den gefundenen Eintrag im Array auf -1 um ihn nicht nochmals als maximales Element zu finden. Wir geben also die Aufgaben der Schwierigkeit nach geordnet aus, die schwierigsten kommen dabei zuerst.

# Beispiele

## Beispiel 0

<aside>
📥

4 7 5

B < A < D < F

D < F < G

A < E < D < C

G < F < C

B C D E F

</aside>

<aside>
📤

C ≥ F ≥ D ≥ B = E 

</aside>

## Beispiel 1

<aside>
📥

4 7 5

A < B < C < D

A < E < C

C < F < D

E < G < F

A C D F G

</aside>

<aside>
📤

D ≥ F ≥ C ≥ G ≥ A 

</aside>

## Beispiel 2

<aside>
📥

6 8 6

A < B < C

E < C < D

E < C < A

E < F < G < H

H < F

D < E

A B D E F G

</aside>

<aside>
📤

G ≥ B ≥ A = E = F ≥ D 

</aside>

## Beispiel 3

<aside>
📥

6 14 14

A < B < C

C < B < D < A < E < F < G

H < I < J < KI < L < H

M < N

N < M

A B C D E F G H I J K L M N

</aside>

<aside>
📤

G ≥ K ≥ M = N ≥ F ≥ J ≥ H ≥ E ≥ L ≥ I ≥ A ≥ D ≥ B = C 

</aside>

## Beispiel 4

<aside>
📥

16 26 5

A < B < C < D < E < J < I

B < C < E < D < I < H < K

S < G < H < I < J

G < H < S < O

M < N < O < K

K < O < M

P < Q < R < F < N < M

S < F < P < N < K

F < T < U

V < W < T < Z

Y < X < Z < T

Z < W < T < V < T < U

K < W < Z < Y

A < B < D < E < W < Z < X < Y < U

R < Q < K < LP < F < K < O < X < W

B W I N F

</aside>

<aside>
📤

W = I = N ≥ B = F 

</aside>

## Beispiel 5

<aside>
📥

11 26 26

H < S < C < A < G

S < O < J < L < F

O < M < X < D < U

C < S < E < N < M

E < M < F < X < B

D < G < P < X < A

R < L < X < U < T

M < O < F < V < D

S < O < U < T < P

Z < Q < K < X < I

B < W < I < Y

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

</aside>

<aside>
📤

Y ≥ A ≥ G ≥ P ≥ X ≥ T ≥ I ≥ U ≥ D ≥ B ≥ W ≥ V ≥ F ≥ M ≥ N ≥ L ≥ K ≥ J ≥ O ≥ Q ≥ C = S ≥ E ≥ H = R = Z 

</aside>

# Quellcode

### Hauptprogramm

```python
# MODE = "ALL" : Ignore relevant tasks from file and order all tasks
# MODE = "SELECTED" : Only order tasks specified in file
MODE = "SELECTED"
np.set_printoptions(precision=3, suppress=True)

# IO
file_name = 
		input("Please provide the path of the .txt-file containing the input: ")
if file_name == "0" or file_name == "1" or file_name == "2" or file_name == "3" 
		or file_name == "4" or file_name == "5":
    # to test the examples given on https://bwinf.de/bundeswettbewerb/43/, 
    # you can just enter the number of the example
    file_name = f"schwierigkeiten{file_name}.txt"
file = open(file_name)

# calculate adjacency-matrix
ad_matr = parse_file(file, mode=MODE)
print(f"\nMatrix A:\n{ad_matr}\n")

# calculate transission-matrix
tr_matr = transition_matrix(ad_matr)
print(f"\nMatrix P:\n{tr_matr}\n")

# calculate random-surfer-matrix
matr = random_surfer(tr_matr, 500)
print(f"\nMatrix Q:\n{matr}\n")

# extract result form random-surfer-matrix and print order
result = matr.sum(0)
print(f"{result} (higher means harder)")
print("\nevaluation:")
evaluate(result.tolist(), mode=MODE, fn=file_name)
```

### Einlesen der Eingabedatei

```python
def parse_file(f, mode):
    lines = f.readlines()
    # reading n, m and k from file, parsing with regex
    params = list(map(int, re.findall(r"\d+", lines[0])))
    n = params[0]  # n is not needed for this implementation
    m = params[1]  # m is the number of tasks
    k = params[2]  # k is the number of tasks to be ordered
    del params
    if mode == "ALL":
        adjacency_matrix = np.identity(m)
        for line in lines[1:-1]:
            if "<" in line:
                # processing the string to create a list, 
                # A < B < C -> ["A", "B", "C"]
                tasks = re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', line)
                for i in range(1, len(tasks)):
                    # < is transitiv, if A < B < C, not only A < B and B < C 
                    # but also A < C are true
                    for j in range(i):
                        adjacency_matrix[ord(tasks[j][0]) - ord("A"), 
		                        ord(tasks[i][0]) - ord("A")] += 1.0
        return adjacency_matrix
    elif mode == "SELECTED":
        adjacency_matrix = np.identity(k)
        selected = re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', lines[-1])
        for line in lines[1:-1]:
            if "<" in line:
                tasks = re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', line)
                tasks[:] = [element for element in 
		                re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', line) if
		                element in selected]
                for i in range(1, len(tasks)):
                    for j in range(i):
                        adjacency_matrix[selected.index(tasks[j][0]), 
		                        selected.index(tasks[i][0])] += 1.0
        return adjacency_matrix
```

### Berechnung der Matrizen

```python
def transition_matrix(adjacency_matrix):
    row_sums = adjacency_matrix.sum(axis=1, keepdims=True)
    return adjacency_matrix / row_sums

def random_surfer(t_matrix, steps):
    matrix = (1 / (steps + 1)) * np.identity(len(t_matrix))
    for i in range(1, steps + 1):
        matrix += (1 / (steps + 1)) * np.linalg.matrix_power(t_matrix, i)
    return matrix
```

### Auswertung und Ausgabe

```python
def evaluate(difficulties, mode, fn):
    if mode == "ALL":
        for j in range(len(difficulties)):
            acc = -1.0
            index = 0
            equal = False
            for i in range(len(difficulties)):
                if acc < difficulties[i]:
                    acc = difficulties[i]
                    equal = False
                    index = i
                elif acc == difficulties[i]:
                    equal = True
            print(f"{chr(index + ord('A'))} ", end="")
            if j < len(difficulties) - 1:
                if equal:
                    print("= ", end="")
                else:
                    print("> ", end="")
            difficulties[index] = -1.0
    elif mode == "SELECTED":
        f = open(fn)
        ls = re.findall(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', f.readlines()[-1])
        for j in range(len(difficulties)):
            acc = -1.0
            index = 0
            equal = False
            for i in range(len(difficulties)):
                if acc < difficulties[i]:
                    acc = difficulties[i]
                    equal = False
                    index = i
                elif acc == difficulties[i]:
                    equal = True
            print(f"{ls[index]} ", end="")
            if j < len(difficulties) - 1:
                if equal:
                    print("= ", end="")
                else:
                    print("> ", end="")
            difficulties[index] = -1.0
```
