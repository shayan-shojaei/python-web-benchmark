import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 100,
  duration: '30s',
};

const port = +__ENV.PORT || 8000;
const database = __ENV.DATABASE || 'mongo'; // 'mongo' || 'postgres'

const baseUrl = `http://localhost:${port}/${database}`;

const itemId = __ENV.ITEM_ID;

const read = () => {
  const url = http.url`${baseUrl}/${itemId}`;
  const res = http.get(url, {
    tags: {
      name: 'read'
    }
  });
}

export default function() {
  read();
}
