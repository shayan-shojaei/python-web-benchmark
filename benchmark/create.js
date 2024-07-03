import http from 'k6/http';

export const options = {
  vus: 100,
  duration: '30s',
};

const port = +__ENV.PORT || 8000;
const database = __ENV.DATABASE || 'mongo'; // 'mongo' || 'postgres'

const baseUrl = `http://localhost:${port}/${database}`;

const generateName = () => {
  return Math.random().toString(36).slice(2, 12);
}

const create = (name) => {
  const url = http.url`${baseUrl}/`;
  const payload = JSON.stringify({ name });
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
    tags: {
      name: 'create',
    }
  };
  const res = http.post(url, payload, params);
  return JSON.parse(res.body)['id'];
}

export default function() {
  const name = generateName()
  create(name);
}
