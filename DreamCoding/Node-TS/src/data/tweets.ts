type Tweet = {
  id: string;
  text: string;
  createdAt: Date;
  name: string;
  username: string;
  url?: string;
};

const tweets: Tweet[] = [
  {
    id: '1',
    text: '성룡이 화이팅!',
    createdAt: new Date(),
    name: 'Bob',
    username: 'bob',
    url: 'https://m.media-amazon.com/images/M/MV5BNzg0MWEyZjItOTZlMi00YmRjLWEyYzctODIwMDU0OThiMzNkXkEyXkFqcGdeQXVyNjUxMjc1OTM@._V1_UY317_CR13,0,214,317_AL_.jpg',
  },
  {
    id: '2',
    text: '드림코딩에서 강의 들으면 너무 좋으다',
    createdAt: new Date(),
    name: 'Seongryong',
    username: 'seongryong',
  },
];

export async function getAll(): Promise<Tweet[]> {
  return tweets;
}
