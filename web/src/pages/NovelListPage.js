import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getNovels } from '@utils/api/apiNovels';
import Cookies from 'universal-cookie';
import Carousel from '../components/Carousel';
import NovelBox from '../components/NovelBox';
import '../css/NovelPage.css';


const cookies = new Cookies();

const NovelListPage = () => {
  const [allNovels, setAllNovels] = useState([]);
  const [expandedNovelId, setExpandedNovelId] = useState(null);
  const [selectedFilter, setSelectedFilter] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchNovels = async () => {
      const token = cookies.get('access_token');
      if (!token) {
        navigate('/login/');
        return;
      }

      try {
        const response = await getNovels();
        setAllNovels(response.novels);
      } catch (error) {
        console.error('Error fetching novels:', error);
        if (error.response && error.response.status === 401) {
          cookies.remove('access_token');
          cookies.remove('refresh_token');
          navigate('/login/');
        }
      }
    };

    fetchNovels();
  }, [navigate]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (expandedNovelId && !event.target.closest('.novel-box')) {
        setExpandedNovelId(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [expandedNovelId]);

  const handleNovelClick = (novelId) => {
    setExpandedNovelId(expandedNovelId === novelId ? null : novelId);
  };

  const handleFilterChange = (event) => {
    setSelectedFilter(event.target.value);
  };

  return (
    <div className="novel-list">
      <div className="carousel-container">
        <Carousel novels={allNovels} expandedNovelId={expandedNovelId} setExpandedNovelId={setExpandedNovelId}/>
      </div>
      <div className="filter">
        <label htmlFor="filter"></label>
        <select
          id="filter"
          value={selectedFilter}
          onChange={handleFilterChange}
        >
          <option value="" disabled hidden>
            Filter by category
          </option>
          <option value="title">Title</option>
          <option value="date">Date</option>
          <option value="popularity">Popularity</option>
        </select>
      </div>
      <div className="tiles-container">
        {allNovels.length > 0 ? (
          allNovels.map((novel) => (
            <NovelBox
              key={novel.id}
              imageUrl={novel.cover_image}
              title={novel.title}
              description={novel.description}
              id={novel.id}
              isExpanded={expandedNovelId === novel.id}
              onClick={() => handleNovelClick(novel.id)}
            />
          ))
        ) : (
          <p>No novels available</p>
        )}
      </div>
    </div>
  );
};

export default NovelListPage;
