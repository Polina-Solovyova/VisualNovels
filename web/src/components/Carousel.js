import React, { useEffect, useState } from 'react';
import { animated } from 'react-spring';
import NovelBox from './NovelBox';

const Carousel = ({ novels }) => {
  const [index, setIndex] = useState(0);
  const [expandedNovelId, setExpandedNovelId] = useState(null);

  const handlePrevClick = () => {
    setIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : novels.length - 1));
  };

  const handleNextClick = () => {
    setIndex((prevIndex) => (prevIndex < novels.length - 1 ? prevIndex + 1 : 0));
  };
  const getNovelIndices = (currentIndex) => {
    const prevIndex = (currentIndex - 1 + novels.length) % novels.length;
    const nextIndex = (currentIndex + 1) % novels.length;

    if (novels.length === 1) return [0, 0, 0];
    if (novels.length === 2) return [0, 0, 1];

    return [prevIndex, currentIndex, nextIndex];
  };

  const [prevIndex, currentIndex, nextIndex] = getNovelIndices(index);

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

  return (
    <div className="carousel-container">
      <button className="carousel-button left" onClick={handlePrevClick}>
        &#8249;
      </button>
      <div className="carousel">
        {[prevIndex, currentIndex, nextIndex].map((novelIndex, i) => {
          const novel = novels[novelIndex] || {};
          const isCenter = i === 1;

          return (
            <animated.div
              key={novel.id || i}
              className={`carousel-item ${expandedNovelId === novel.id ? 'expanded' : ''}`}
              style={{
                transform: isCenter ? 'scale(1)' : 'scale(0.8)',
                filter: isCenter ? 'brightness(1)' : 'brightness(0.7) blur(1px)',
                boxShadow: isCenter ? '0 0 50px rgba(0,0,0,0.8)' : 'inset 0 0 60px #1C1642FF',
                borderRadius: isCenter ? '20px' : '20px',
                zIndex: isCenter ? '900' : '500',
              }}
            >
              <NovelBox
                imageUrl={novel.cover_image}
                title={novel.title || 'Untitled'}
                description={novel.description || 'No description available'}
                id={novel.id}
                isExpanded={expandedNovelId === novel.id}
                onClick={() => handleNovelClick(novel.id)}
              />
            </animated.div>
          );
        })}
      </div>
      <button className="carousel-button right" onClick={handleNextClick}>
        &#8250;
      </button>
    </div>
  );
};

export default Carousel;
