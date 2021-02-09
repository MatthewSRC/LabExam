class ExamException(Exception):
  pass

# Classe file reader
class CSVTimeSeriesFile:

  # Inizializzazione con passaggio del parametro "nome" del file
  def __init__(self, name):
    # Primo controllo, controllo che sia un valore string, che non sia vuota e che abbia '.' nel nome
    if not isinstance(name, str) or name == '' or '.' not in name:
      raise ExamException('Errore, nome file non valido')
      
    self.name = name

  # Funzione per prendere i dati
  def get_data(self):
    # Inizializzo array vuoto
    data = []

    # Secondo controllo sul nome del file, utilizzo un try except per controllare che tutto fili liscio
    try:
      my_file = open(self.name, "r") 
    except:
      # Alzo un errore in caso del file inesistente o non leggibile
      raise ExamException('Errore, file inesistente o non leggibile')

    for line in my_file:
      elements = line.split(',')

      # Salto la linea in caso sia l'intestazione
      if elements[0] != 'epoch':
        epoch = 0
        temp = 0
        
        # Controllo che i valori siano validi e converto in int e float silenziosamente
        try:
          epoch = int(elements[0])
          temp = float(elements[1])
        except:
          # In caso di errori salto la riga
          continue

        # Se sono ordinati, so che posso controllare solamente gli ultimi due valori
        if data:
          # Prendo l'ultimo epoch
          lastEpoch = data[len(data) - 1][0]

          if lastEpoch > epoch:
            raise ExamException('Errore, epoch fuori ordine')
          
          # Avrei potuto mettere nel controllo sopra >= per abbreviare il codice e dare in entrambi i casi un solo errore, ma ho preferito differenziarli
          if lastEpoch == epoch:
            raise ExamException('Errore, epoch duplicato')

        my_data = [ epoch, temp ]
        data.append(my_data)

    # Controllo che ci sia almeno un dato    
    if len(data) == 0:
      raise ExamException('Errore, lista valori non valda')

    return data

# Classe contenente le funzioni da utilizzare in seguito
class FunctionsHelper:

  # Definisco la classe passando come parametro vals (array di float)
  def __init__(self, vals):
    self.vals = vals

  # Calcolo la media
  def avg(self):
    sum = 0.0

    for v in self.vals:
      sum += v

    # Non devo controllare che non sia / 0 perchè ogni giorno ha almeno un dato (da testo)
    return sum / len(self.vals)

  # Calcolo il massimo
  def max(self):
    max = self.vals[0]
    
    for v in self.vals:
      if v > max:
        max = v

    return max
  
  # Calcolo il minimo
  def min(self):
    min = self.vals[0]

    for v in self.vals:
      if v < min:
        min = v

    return min

# Funzione per ottenere la temperatura in ordine: Minima, Massima e Media
def daily_stats(time_series):
  # Inizializzo array vuota
  stats = []

  # Utilizzo il for con la funziona splitDays per ottenere le temperature suddivise per giorni
  for v in splitDays(time_series):
    # Inizializzo la class FunctionsHelper che mi servirà per usare le funzioni
    # Min, Max e Avg
    func = FunctionsHelper(v)
    stats.append([ func.min(), func.max(), func.avg() ])
  return stats

# Funzione per dividere i valori per giorni
# Ogni sotto-array è un giorno
def splitDays(time_series):
  # Inizializzo array vuota
  days = []

  # Inizializzo variabile a None per tenere l'informazione sull'ultimo giorno
  # che sto valutando
  lastDay = None

  for v in time_series:
    # Prendo valore epoch dall'array
    epoch = v[0]
    # Prendo valore temperatura dall'array
    temp = v[1]
    # Calcolo l'epoch dell'inizio del giorno corrente
    day_start_epoch = epoch - (epoch % 86400)

    # Controllo che lastDay (ultimo giorno salvato) sia none o diverso dal day_start_epoch (giorno corrente)
    if lastDay is None or day_start_epoch != lastDay:
      # In questo caso so che sono passato ad un nuovo giorno
      days.append([temp])
      lastDay = day_start_epoch
    else:
      # Prendo il giorno su cui sto lavorando e ci aggiungo la temperatura
      days[len(days) - 1].append(temp)
  return days

# Carico i valori
time_series_file = CSVTimeSeriesFile(name='data.csv')

time_series = time_series_file.get_data()