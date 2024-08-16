import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getNovelDetails } from '@utils/api/apiNovels';

const NovelDetail = () => {
  const { id } = useParams();
  const [novel, setNovel] = useState(null);

  useEffect(() => {
    async function fetchNovel() {
      try {
        const response = await getNovelDetails(id);
        setNovel(response);
      } catch (error) {
        console.error(error);
      }
    }
    fetchNovel();
  }, [id]);

  if (!novel) return <div>Loading...</div>;

  return (
    <div className="novel-detail">
      <h1>{novel.title}</h1>
      <img src={novel.cover_image} alt={novel.title} />
      <p>{novel.description}</p>
      <Link to={`/novel/${id}/read`} className="start-reading-button">
        Start Reading
      </Link>
    </div>
  );
};

export default NovelDetail;
