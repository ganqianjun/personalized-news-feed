import './NewsCard.css';
import React from 'react';

class NewsCard extends React.Component {
  redirectToUrl(url) {
    window.open(url, '_blank');
  }

  render() {
    // news is in NewsPanel so NewsCard only need to show it
    return (
      <div className="news-container"
           onClick={() => this.redirectToUrl(this.props.news.url)}>
        <div className='row'>
          <div className='col s4 fill'>
            <img src={this.props.news.urlToImage} alt='news'/>
          </div>
          <div className="col s8">
            <div className="news-intro-col">
              <div className="news-intro-panel">
                <h4>{this.props.news.title}</h4>
                <div className="news-description">
                  <p>{this.props.news.description}</p>
                  <div>
                    {
                      this.props.news.source != null &&
                      <div className='chip light-blue news-chip'>
                        {this.props.news.source}
                      </div>
                    }
                    {
                      this.props.news.reason != null &&
                      <div className='chip light-green news-chip'>
                        {this.props.news.reason}
                      </div>
                    }
                    {
                      this.props.news.time != null &&
                      <div className='chip amber news-chip'>
                        {this.props.news.time}
                      </div>
                    }
                  </div>
                </div> {/* End of news-description */}
              </div> {/* End of 'news-intro-panel'*/}
            </div> {/* End of 'news-intro-col'*/}
          </div> {/* End of 'col s8'*/}
        </div> {/* End of 'row'*/}
      </div> 
    );
  }
}

export default NewsCard;
