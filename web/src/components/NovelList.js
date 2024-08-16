import React from 'react';
import NovelBox from './NovelBox';

const NovelList = ({ novels, expandedNovelId, handleNovelClick }) => {
  return (
    <div className="tiles-container">
      {novels.length > 0 ? (
        novels.map((novel) => (
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
  );
};

export default NovelList;
