class Seq:
    """
    Хранит одну биологическую последовательность и ее заголовок.
    """
    def __init__(self, head, sequence):
        self.sequence = sequence
        # sequence - сама нуклеотидная последовательность или аминокислоты
        self.head = head
        # header - строка после '>' в fasta файле
    def length(self):
        """ Возвращает длину последовательности
        """
        return len(self.sequence)
    def __str__(self):
        """ Красивый вывод в формате Fasta. Разбиваем строку по 60 символов.
        """
        lines = []
        for i in range(0, len(self.sequence), 60):
            piece = self.sequence[i:i+60]
            lines.append(piece)
        return f'>{self.head}\n' + '\n'.join(lines)
    def alphabet(self):
        """ Определяем алфавит последовательности: нуклеотидный или белковый.
        """
        protein_letters = 'EFILPQZJXO*'
        for letter in self.sequence:
            if letter in protein_letters:
                return 'Это белковая последовательность'
        return 'Это нуклеотидная последовательность'
class FastaReader:
    """ Читает файл построчно, по одной записи выдает объекты Seq. Использует генератор - в памяти только один из объектов.
    """
    def __init__(self, path):
        self.path = path
    def true_fasta(self):
        """ Проверяет на соответствие формату Fasta. Первая непустая строка должна начинаться с символа '>'.
        """
        with open(self.path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() == '': # пропуск пустых строк
                    continue
                return line.startswith('>')
        return False
    def __iter__(self):
        """Генератор: выдает по одному объекту Seq за один раз
        """
        header = None
        seq_parts = []
        with open(self.path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                if line.startswith('>'):
                    # когда встретили новый заголовок - отдаем предыдущий
                    if header is not None:
                        yield Seq(header, ''.join(seq_parts))
                    header = line[1:]     # убираем ">"
                    seq_parts = []
                else:
                    seq_parts.append(line)
            if header is not None:
                yield Seq(header, ''.join(seq_parts)) # отдаем последнюю запись
if __name__ == '__main__':
    reader = FastaReader('test.fasta')
    if not reader.true_fasta():
        print('Это не fasta-файл!')
    else:
        print('Файл валидный')
        for seq in reader:
            print(seq)
            print('Длина:',seq.length())
            print('Алфавит:', seq.alphabet())
