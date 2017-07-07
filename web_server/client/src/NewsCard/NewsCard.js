import './NewsCard.css';

import Auth from '../Auth/Auth';
import React from 'react';

class NewsCard extends React.Component {
  constructor() {
    super();
    this.redirectToUrl = this.redirectToUrl.bind(this);
   }

   redirectToUrl(event) {
     event.preventDefault();
     this.sendClickLog();
     window.open(this.props.news.url, '_blank');
   }

  sendClickLog() {
    let url = 'http://localhost:3000/news/userId/' + Auth.getEmail()
              + '/newsId/' + this.props.news.digest;

    let request = new Request(encodeURI(url), {
      method: 'POST',
      headers: {
        'Authorization': 'bearer ' + Auth.getToken(),
      },
      cache: false});
    fetch(request);
  }

  render() {
    // news is in NewsPanel so NewsCard only need to show it
    return (
      <div className="news-container" onClick={this.redirectToUrl}>
        <div className='row'>
          <div className='col s12 m5 fill'>
            <img src={this.props.news.urlToImage} alt='news'/>
          </div>
          <div className="col s12 m7">
            <div className="news-intro-col">
              <div className="news-intro-panel">
                <h5>{this.props.news.title}</h5>
                <div className="news-description">
                  <p>{this.props.news.description}</p>
                  <div>
                    {
                      this.props.news.source != null &&
                      <div className='chip light-blue lighten-3 news-chip'>
                        {this.props.news.source}
                      </div>
                    }
                    {
                      this.props.news.reason != null &&
                      <div className='chip amber lighten-3 news-chip'>
                        {this.props.news.reason}
                      </div>
                    }
                    {
                      this.props.news.time != null &&
                      <div className='chip light-green lighten-3 news-chip'>
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
