import { useState, useEffect } from "react";

function App() {
  const [city, setCity] = useState("");
  const [newsList, setNewsList] = useState<string[]>([]);
  const [selectedNews, setSelectedNews] = useState("");
  const [loadingHeadline, setLoadingHeadline] = useState<boolean>(false);
  const [summaryStatus, setSummaryStatus] = useState<boolean>(false);

  interface RedditComment {
    Subreddit: string;
    PostTitle: string;
    CommentBody: string;
    PostAge: number;
    Author: string;
    Score: number;
  }

  const [redditList, setRedditList] = useState<RedditComment[]>([]);

  interface SummaryResultType {
    summary: string;
    sentiment: string;
    actionable_needs: string;
  }

  const [summaryResult, setSummaryResult] = useState<SummaryResultType>({
    summary: "",
    sentiment: "",
    actionable_needs: "",
  });

  function handleFetchComments() {
    if (selectedNews) {
      fetchComments(selectedNews);
    }
  }

  function fetchComments(newsTitle: string) {
    setSummaryStatus(true);

    fetch("http://localhost:8000/fetch-comments/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ topic: newsTitle }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("data comm", data);
        setRedditList(data.comments);
        setSummaryResult({
          summary: data.summary,
          sentiment: data.sentiment,
          actionable_needs: data.actionable_needs,
        });
        setSummaryStatus(false);
      })
      .catch((error) => {
        console.error("Error fetching comments:", error);
        alert("error fetching summary");
        setSummaryStatus(false);
      });
  }

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (city) {
        setLoadingHeadline(true);
        fetch(`http://localhost:8000/fetch-news/?city=${city}`)
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then((data) => {
            setNewsList(data.top_news);
            if (data.top_news.length > 0) {
              setSelectedNews(data.top_news[0]);
            }
            setLoadingHeadline(false);
          })
          .catch((error) => {
            console.error("Error fetching news:", error);
            alert(`Error fetching news`);
            setLoadingHeadline(false);
          });
      }
    }, 500);

    return () => clearTimeout(delayDebounceFn);
  }, [city]);

  interface SummaryCardProps {
    summaryResult: SummaryResultType;
  }

  const SummaryCard: React.FC<SummaryCardProps> = ({ summaryResult }) => {
    return (
      <div className="my-8 flex max-w-screen-lg flex-col rounded-xl border border-gray-100 p-6 text-gray-600 shadow-lg sm:p-8">
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Summary</h3>
          <p className="text-sm mt-2">{summaryResult.summary}</p>
        </div>

        <div className="mb-4">
          <h3 className="text-lg font-semibold">Sentiment</h3>
          <p className="text-sm mt-2">{summaryResult.sentiment}</p>
        </div>

        <div>
          <h3 className="text-lg font-semibold">Actionable Needs</h3>
          <ul className="list-disc list-inside mt-2 text-sm">
            {summaryResult.actionable_needs
              .split("\n")
              .map((item: string, index: number) => (
                <li key={index}>{item}</li>
              ))}
          </ul>
        </div>
      </div>
    );
  };

  return (
    <section className="shadow-blue-100 mx-auto max-w-screen-lg rounded-xl bg-white text-gray-600 shadow-lg sm:my-10 sm:border">
      <div className="container mx-auto flex flex-col flex-wrap px-5 pb-12">
        <div className="bg-slate-50 mx-auto mt-4 mb-10 flex w-full flex-wrap items-center space-x-4 py-4 md:mb-20 md:justify-center md:px-10">
          <svg
            className="flex h-8 w-8 items-center justify-center "
            xmlns="http://www.w3.org/2000/svg"
            x="0px"
            y="0px"
            width="100"
            height="100"
            viewBox="0 0 50 50"
          >
            <path d="M 1.9375 2.78125 C 1.386719 2.78125 0.9375 3.230469 0.9375 3.78125 L 0.9375 39.46875 C 0.9375 42.082031 1.699219 44.1875 3.25 45.71875 C 5.714844 48.15625 9.242188 48.21875 9.59375 48.21875 L 41.375 48.21875 C 41.429688 48.21875 41.773438 48.226563 42.25 48.15625 C 39.136719 47.761719 34.625 45.617188 34.625 39.46875 L 34.625 3.78125 C 34.625 3.230469 34.179688 2.78125 33.625 2.78125 Z M 36.625 9.5 L 36.625 39.46875 C 36.625 46.113281 43.039063 46.21875 43.3125 46.21875 C 43.851563 46.214844 48.3125 46.011719 49 40.90625 C 49.046875 40.472656 49.0625 40.019531 49.0625 39.53125 L 49.0625 14.4375 C 49.0625 14.433594 49.0625 14.410156 49.0625 14.40625 C 49.027344 12.957031 48.25 10.414063 45.65625 9.71875 C 44.84375 9.914063 44.167969 10.277344 43.65625 10.8125 C 42.332031 12.195313 42.375 14.324219 42.375 14.34375 L 42.375 38.625 C 42.375 39.179688 41.929688 39.625 41.375 39.625 C 40.820313 39.625 40.375 39.179688 40.375 38.625 L 40.375 14.375 C 40.371094 14.300781 40.273438 11.511719 42.125 9.5 Z M 7.21875 11 L 26.9375 11 C 27.492188 11 27.9375 11.449219 27.9375 12 C 27.9375 12.550781 27.492188 13 26.9375 13 L 7.21875 13 C 6.667969 13 6.21875 12.550781 6.21875 12 C 6.21875 11.449219 6.667969 11 7.21875 11 Z M 7.21875 15 L 26.9375 15 C 27.492188 15 27.9375 15.449219 27.9375 16 C 27.9375 16.550781 27.492188 17 26.9375 17 L 7.21875 17 C 6.667969 17 6.21875 16.550781 6.21875 16 C 6.21875 15.449219 6.667969 15 7.21875 15 Z M 7.6875 23 L 14.46875 23 C 15.019531 23 15.46875 23.449219 15.46875 24 C 15.46875 24.550781 15.019531 25 14.46875 25 L 7.6875 25 C 7.136719 25 6.6875 24.550781 6.6875 24 C 6.6875 23.449219 7.136719 23 7.6875 23 Z M 19.21875 23 L 26.9375 23 C 27.492188 23 27.9375 23.449219 27.9375 24 C 27.9375 24.550781 27.492188 25 26.9375 25 L 19.21875 25 C 18.667969 25 18.21875 24.550781 18.21875 24 C 18.21875 23.449219 18.667969 23 19.21875 23 Z M 7.6875 27 L 14.46875 27 C 15.019531 27 15.46875 27.445313 15.46875 28 C 15.46875 28.554688 15.019531 29 14.46875 29 L 7.6875 29 C 7.136719 29 6.6875 28.554688 6.6875 28 C 6.6875 27.445313 7.136719 27 7.6875 27 Z M 19.21875 27 L 26.9375 27 C 27.492188 27 27.9375 27.445313 27.9375 28 C 27.9375 28.554688 27.492188 29 26.9375 29 L 19.21875 29 C 18.667969 29 18.21875 28.554688 18.21875 28 C 18.21875 27.445313 18.667969 27 19.21875 27 Z M 19.21875 30.78125 L 26.9375 30.78125 C 27.492188 30.78125 27.9375 31.226563 27.9375 31.78125 C 27.9375 32.335938 27.492188 32.78125 26.9375 32.78125 L 19.21875 32.78125 C 18.667969 32.78125 18.21875 32.335938 18.21875 31.78125 C 18.21875 31.226563 18.667969 30.78125 19.21875 30.78125 Z M 7.6875 31 L 14.46875 31 C 15.019531 31 15.46875 31.445313 15.46875 32 C 15.46875 32.554688 15.019531 33 14.46875 33 L 7.6875 33 C 7.136719 33 6.6875 32.554688 6.6875 32 C 6.6875 31.445313 7.136719 31 7.6875 31 Z M 19.21875 34.78125 L 26.9375 34.78125 C 27.492188 34.78125 27.9375 35.226563 27.9375 35.78125 C 27.9375 36.335938 27.492188 36.78125 26.9375 36.78125 L 19.21875 36.78125 C 18.667969 36.78125 18.21875 36.335938 18.21875 35.78125 C 18.21875 35.226563 18.667969 34.78125 19.21875 34.78125 Z M 7.6875 35 L 14.46875 35 C 15.019531 35 15.46875 35.445313 15.46875 36 C 15.46875 36.554688 15.019531 37 14.46875 37 L 7.6875 37 C 7.136719 37 6.6875 36.554688 6.6875 36 C 6.6875 35.445313 7.136719 35 7.6875 35 Z M 19.21875 38.53125 L 26.9375 38.53125 C 27.492188 38.53125 27.9375 38.976563 27.9375 39.53125 C 27.9375 40.085938 27.492188 40.53125 26.9375 40.53125 L 19.21875 40.53125 C 18.667969 40.53125 18.21875 40.085938 18.21875 39.53125 C 18.21875 38.976563 18.667969 38.53125 19.21875 38.53125 Z M 7.6875 39 L 14.46875 39 C 15.019531 39 15.46875 39.445313 15.46875 40 C 15.46875 40.554688 15.019531 41 14.46875 41 L 7.6875 41 C 7.136719 41 6.6875 40.554688 6.6875 40 C 6.6875 39.445313 7.136719 39 7.6875 39 Z"></path>
          </svg>
          <span className="text-black text-3xl font-bold md:inline">
            City Discussion Dashboard
          </span>
        </div>

        <div className="flex w-full flex-col">
          <h1 className="text-2xl font-semibold">
            Find out the current ongoing hot news in your city now !!
          </h1>
          <p className="mt-2 text-gray-500">
            Enter your city name and get the report in one click
          </p>
          <div className="mt-4 grid items-center gap-3 gap-y-5 sm:grid-cols-4">
            <div className="flex flex-col sm:col-span-3">
              <label
                className="mb-1 my-4 font-semibold text-gray-500"
                htmlFor="cityInput"
              >
                Enter City
              </label>
              <input
                type="text"
                id="cityInput"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="rounded-lg border px-2 py-2 mt-2 shadow-sm outline-none focus:ring"
              />
              {loadingHeadline ? (
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-4 h-4 border-t-2 border-blue-700 rounded-full animate-spin"></div>
                </div>
              ) : (
                newsList.length > 0 && (
                  <div className="flex flex-col">
                    <label
                      className="mb-1 my-4 font-semibold text-gray-500"
                      htmlFor="newsSelect"
                    >
                      Select Headline
                    </label>
                    <select
                      id="newsSelect"
                      className="rounded-lg border px-2 py-2 mt-2 shadow-sm outline-none focus:ring"
                      value={selectedNews}
                      onChange={(e) => setSelectedNews(e.target.value)}
                    >
                      {newsList.map((news, index) => (
                        <option key={index} value={news}>
                          {news}
                        </option>
                      ))}
                    </select>

                    <div className="flex flex-col justify-between sm:flex-row">
                      <button
                        className="group my-6 flex w-full items-center justify-center rounded-lg bg-blue-700 py-2 text-center font-bold text-white outline-none transition sm:order-1 sm:w-40 focus:ring"
                        onClick={handleFetchComments}
                      >
                        Continue
                      </button>
                    </div>
                  </div>
                )
              )}
            </div>
          </div>

          {/* reddit discussion report */}
          {summaryStatus ? (
            <div className="flex justify-center items-center">
              <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-blue-500 border-solid"></div>
            </div>
          ) : (
            <>
              {redditList?.length > 0 && (
                <div className="my-8 flex flex-col max-w-screen-sm rounded-xl border border-gray-100 p-4 text-left text-gray-600 shadow-lg sm:p-8">
                  {/* Reddit Discussion Report */}
                  <div className="my-8 flex max-w-screen-sm flex-col rounded-xl border border-gray-100 p-4 text-left text-gray-600 shadow-lg sm:p-8">
                    <h1 className="text-sm text-blue-600 sm:text-2xl">
                      Reddit Discussion on the selected News
                    </h1>
                    {redditList.map((comment, index) => (
                      <div key={index} className="w-full text-left mb-4">
                        <div className="mb-2 flex flex-col justify-between text-gray-600 sm:flex-row"></div>
                        <h2 className="font-medium">{comment.Subreddit}</h2>
                        <h3 className="font-medium">{comment.PostTitle}</h3>
                        <p className="text-sm mb-2">{comment.CommentBody}</p>
                        <div className="flex items-center justify-between text-gray-600">
                          <p className="text-xs">{comment.PostAge} days ago</p>
                          <h3 className="font-medium">{comment.Author}</h3>
                          <a
                            title="Likes"
                            href="#"
                            className="group flex cursor-pointer items-center justify-around"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              className="h-6 w-6 rounded-full p-1 group-hover:bg-red-200 group-hover:text-red-500"
                              fill="none"
                              viewBox="0 0 24 24"
                              stroke="currentColor"
                              strokeWidth="2"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                              />
                            </svg>
                            {comment.Score}
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                  {summaryResult && (
                    <SummaryCard summaryResult={summaryResult} />
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </section>
  );
}

export default App;
