"""Original AI-assisted k-nearest-neighbors classifier; standard library only."""
import csv
from pathlib import Path

LABELS = ('Support', 'Standard', 'Challenge')

class LayoutModel:
    def __init__(self, path=None):
        path = Path(path) if path else Path(__file__).with_name('training_data.csv')
        with path.open(newline='', encoding='utf-8') as stream:
            self.rows = [(float(r['accuracy']), float(r['hint_rate']), r['layout'])
                         for r in csv.DictReader(stream)]
        if len(self.rows) < 3 or any(r[2] not in LABELS for r in self.rows):
            raise ValueError('Training file needs at least three valid labeled examples.')

    def predict(self, accuracy, hint_rate):
        if not all(0 <= x <= 1 for x in (accuracy, hint_rate)):
            raise ValueError('Features must be in [0, 1].')
        nearest = sorted(enumerate(self.rows), key=lambda pair:
                         ((pair[1][0]-accuracy)**2 + (pair[1][1]-hint_rate)**2, pair[0]))[:3]
        votes = {label: sum(row[2] == label for _, row in nearest) for label in LABELS}
        # Prefer Standard for tied votes, then Support, then Challenge.
        label = max(('Standard', 'Support', 'Challenge'), key=lambda s: votes[s])
        return label, votes[label] / 3

class Session:
    def __init__(self, model=None):
        self.model = model or LayoutModel()
        self.history = []
        self.override = 'Auto'

    def record(self, correct, used_hint):
        self.history.append((bool(correct), bool(used_hint)))
        self.history = self.history[-5:]

    def decision(self):
        n = len(self.history)
        accuracy = sum(x[0] for x in self.history) / n if n else 0
        hints = sum(x[1] for x in self.history) / n if n else 0
        if self.override != 'Auto':
            return self.override, 'Manual choice. Select Auto to resume adaptation.'
        if n < 3:
            return 'Standard', f'Collecting evidence: {n}/3 answers. No ability assessment.'
        label, agreement = self.model.predict(accuracy, hints)
        return label, (f'Last {n} answers: {accuracy:.0%} correct; {hints:.0%} used hints. '
                       f'Nearest-example vote: {agreement:.0%}; not calibrated confidence.')
