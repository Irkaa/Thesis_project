export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function fetchAPI(endpoint) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (err) {
    console.error("API Fetch Error:", err.message);
    return null;
  }
}
