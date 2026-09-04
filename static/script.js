const form = document.querySelector('#process-form');
const fileInput = document.querySelector('#image-file');
const fileLabel = document.querySelector('#file-label');
const statusText = document.querySelector('#status');
const emptyResult = document.querySelector('#empty-result');
const resultContent = document.querySelector('#result-content');
const resultImage = document.querySelector('#result-image');
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

    resultImage.src = `${data.image_url}?t=${Date.now()}`;
    countsContainer.replaceChildren();
    Object.entries(data.counts).forEach(([key, value]) => {
      const item = document.createElement('div');
      item.className = 'count-item';
      item.innerHTML = `<strong>${value}</strong><span>${labels[key]}</span>`;
      countsContainer.append(item);
    });
    emptyResult.hidden = true;
    resultContent.hidden = false;
    statusText.textContent = 'Готово. Результат сохранён в истории.';
  } catch (error) {
    statusText.textContent = error.message;
  }
});

historyButton.addEventListener('click', async () => {
  if (!historyContent.hidden) {
    historyContent.hidden = true;
    historyButton.textContent = 'Показать историю';
    return;
  }

  historyButton.disabled = true;
  historyButton.textContent = 'Загрузка...';
  try {
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
    historyContent.hidden = false;
    historyButton.textContent = 'Скрыть историю';
  } catch (error) {
    statusText.textContent = error.message;
    historyButton.textContent = 'Показать историю';
  } finally {
    historyButton.disabled = false;
  }
});
