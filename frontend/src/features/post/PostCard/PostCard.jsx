import { Link, useNavigate } from 'react-router-dom';
import style from './style.module.css'

function PostCard({ authorname, authorUsername, posttitle, postdescription="", img_list=[], postId, onImageClick }){
    const navigate = useNavigate();
    const images = img_list.length > 0 ? img_list : [{ url: "static/images/506302782_9643445375778926_6296838114955530405_n.jpg" }];
    const count = images.length;
    
    const getGridClass = () => {
        if (count === 1) return style.singleImage;
        if (count === 2) return style.twoImages;
        if (count === 3) return style.threeImages;
        if (count === 4) return style.fourImages;
        return style.manyImages;
    };

    const handleImageClick = (img_data, index) => {
        if (onImageClick) {
            onImageClick(postId, img_data, index);
        } else if (postId) {
            navigate(`/post/${postId}`);
        }
    };

    return (
        <div className={style.postcard}>
            <div className={style.postheading}>
                <div className={style.postauthor}>
                    {authorUsername ? (
                        <Link to={`/${authorUsername}`} className={style.authorname}>{authorname}</Link>
                    ) : (
                        <span className={style.authorname}>{authorname}</span>
                    )}
                </div>
                {/* <button>close</button> */}
            </div>
            <div className={style.postcontent}>
                <div className={style.posttitle}>{posttitle}</div>
                <div className={style.postdescription}>{postdescription}</div>
                <div className={`${style.imageGrid} ${getGridClass()}`}>
                    {images.slice(0, count === 1 ? 1 : 4).map((img_data, index) => (
                        <div key={index} className={style.imageWrapper}>
                            <img 
                                src={img_data.url} 
                                alt="" 
                                className={style.postimage} 
                                onClick={() => handleImageClick(img_data, index)}
                                style={{ cursor: 'pointer' }}
                            />
                            {index === 3 && count > 4 && (
                                <div className={style.moreOverlay}>
                                    <span>+{count - 4}</span>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
            <div className={style.postfooter}>
                <div className={style.reactionbuttons}>
                    <button>Like</button>
                    <button>Comment</button>
                    <button>Share</button>
                </div>
                <div className={style.totalreactions}>
                    <span>10 Likes</span>
                    <span>2 Comments</span>
                    <span>0 Shares</span>
                </div>
            </div>
        </div>
    )
}

export {PostCard}
