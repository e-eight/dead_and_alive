from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import numpy as np


class QuantumDice:
    def __init__(self, base=20):
        self.base = base
        self.qubits = int(np.ceil(np.log2(base)))

    def _generate_circuit(self):
        qc = QuantumCircuit(self.qubits)
        qc.h(list(range(self.qubits)))
        qc.measure_all()
        return qc

    def _measure(self, backend="qasm_simulator"):
        qc = self._generate_circuit()
        backend = Aer.get_backend(backend)
        result = execute(qc, backend, shots=1).result()
        roll = [k for k in result.get_counts().keys()][0]
        return roll

    def roll(self, backend="qasm_simulator", modular=True):
        bit = [int(c) for c in self._measure()]
        dec = 0
        for i in range(self.qubits):
            dec = dec + bit[i] * 2**(self.qubits - i - 1)
        rolled = (dec + 1)

        if modular:
            rolled = rolled % self.base
            if rolled == 0:
                rolled = self.base
        else:
            max_roll = 2**self.qubits
            rolled = np.ceil(rolled * self.base / max_roll)
            rolled = int(rolled)
        return rolled
