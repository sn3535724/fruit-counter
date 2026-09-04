const form = document.querySelector('#process-form');
const fileInput = document.querySelector('#image-file');
const fileLabel = document.querySelector('#file-label');
const statusText = document.querySelector('#status');
const resultContainer = document.querySelector('#result');
const countsContainer = document.querySelector('#counts');
const historyButton = document.querySelector('#history-button');
const historyContent = document.querySelector('#history-content');
const historyList = document.querySelector('#history-list');

const labels = {
  apple: 'Яблоки',
  banana: 'Бананы',
  orange: 'Апельсины',
  total: 'Всего',
};

fileInput.addEventListener('change', () => {
  fileLabel.textContent = fileInput.files[0]?.name || 'Выберите файл';
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!fileInput.files[0]) return;

  const formData = new FormData(form);
  statusText.textContent = 'Модель обрабатывает изображение...';

  try {
    const response = await fetch('/process', { method: 'POST', body: formData });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Не удалось обработать файл');

    resultContainer.replaceChildren();
    const resultImage = document.createElement('img');
    resultImage.src = `${data.image_url}?t=${Date.now()}`;
    resultImage.alt = 'Обработанное изображение';
    resultContainer.append(resultImage);

    countsContainer.replaceChildren();
    Object.entries(data.counts).forEach(([key, value]) => {
      const item = document.createElement('div');
      item.className = 'count-item';
      const valueElement = document.createElement('strong');
      valueElement.textContent = value;
      const labelElement = document.createElement('span');
      labelElement.textContent = labels[key];
      item.append(valueElement, labelElement);
      countsContainer.append(item);
    });
    countsContainer.hidden = false;
    if (!historyContent.hidden) await loadHistory();
    statusText.textContent = 'Готово. Результат сохранён в истории.';
  } catch (error) {
    statusText.textContent = error.message;
  }
});

async function loadHistory() {
  const response = await fetch('/history');
  if (!response.ok) throw new Error('Не удалось загрузить историю');
  const history = await response.json();
  historyList.replaceChildren();
  history.forEach((entry) => {
    const row = document.createElement('tr');
    [entry.timestamp, entry.apple, entry.banana, entry.orange, entry.total]
      .forEach((value) => {
        const cell = document.createElement('td');
        cell.textContent = value;
        row.append(cell);
    });
    historyList.append(row);
  });
}

historyButton.addEventListener('click', async () => {
  if (!historyContent.hidden) {
    historyContent.hidden = true;
    historyButton.textContent = 'Показать историю';
    return;
  }

  historyButton.disabled = true;
  historyButton.textContent = 'Загрузка...';
  try {
    await loadHistory();
    historyContent.hidden = false;
    historyButton.textContent = 'Скрыть историю';
  } catch (error) {
    statusText.textContent = error.message;
    historyButton.textContent = 'Показать историю';
  } finally {
    historyButton.disabled = false;
  }
});
