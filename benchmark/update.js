import http from 'k6/http';

export const options = {
  vus: 100,
  duration: '30s',
};

const port = +__ENV.PORT || 8000;
const database = __ENV.DATABASE || 'mongo'; // 'mongo' || 'postgres'

const baseUrl = `http://localhost:${port}/${database}`;

const itemId = __ENV.ITEM_ID;

const generateName = () => {
  return Math.random().toString(36).slice(2, 12);
}

const update = (name) => {
  const url = http.url`${baseUrl}/${itemId}`;
  const payload = JSON.stringify({ name });
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
    tags: {
      name: 'update'
    }
  };
  const res = http.put(url, payload, params);
} 

export default function() {
  const updatedName = generateName();
  update(updatedName);
}
