class HttpError extends Error {
  constructor(statusCode, title, data) {
    super(HttpError.makeMessage(statusCode, title, data));
    this.statusCode = statusCode;
    this.title = title;
    this.info = data;
  }

  static makeMessage(statusCode, title, data) {
    let message = '';

    message += statusCode ? `${statusCode} - ` : '(unknown status code) - ';
    message += title ? `${title} - ` : '(unknown error message) - ';
    message += data.detail
      ? 'Error located in: ' + `${JSON.stringify(data.detail[0].loc)}` + ', ' + `${data.detail[0].msg}`
      : data.error
        ? `${data.error}`
        : '(unknown error detail)';

    return message;
  }
}

class NetworkError extends Error {
  constructor(message) {
    super(message);
  }
}

class UnexpectedError extends Error {
  constructor(message) {
    super(message);
  }
}

export default function handleError(error) {
  if (error.response) {
    throw new HttpError(error.response.status, error.response.statusText, error.response.data);
  } else if (error.request) {
    throw new NetworkError('Impossible to contact the server. Check your internet connection.');
  } else {
    throw new UnexpectedError(`${error.message}`);
  }
}
