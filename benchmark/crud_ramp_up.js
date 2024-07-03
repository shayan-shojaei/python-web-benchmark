import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m30s', target: 100 },
    { duration: '20s', target: 0 },
  ],
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

const read = (id) => {
  const url = http.url`${baseUrl}/${id}`;
  const res = http.get(url, {
    tags: {
      name: 'read'
    }
  });
}

const update = (id, name) => {
  const url = http.url`${baseUrl}/${id}`;
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

const del = (id) => {
  const url = http.url`${baseUrl}/${id}`;
  const res = http.del(url, {
    tags: {
      name: 'delete'
    }
  });
}

export default function() {
  const name = generateName()
  const id = create(name);

  read(id);

  const updatedName = generateName();
  update(id, updatedName);

  del(id);
}
