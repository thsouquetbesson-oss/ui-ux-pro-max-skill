// storage.js — LocalStorage persistence layer
// Handles serialization/deserialization of app state

const STORAGE_KEY = 'trail-data';

export function loadData() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
  } catch {
    return null;
  }
}

export function saveData(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}
