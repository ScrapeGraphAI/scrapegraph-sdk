class HttpError extends Error {
  constructor(statusCode, title, detail) {
    super(HttpError.makeMessage(statusCode, title, detail));
    this.statusCode = statusCode;
    this.title = title;
    this.detail = detail;
  }

  static makeMessage(statusCode, title, detail) {
    let message = '';

    message += statusCode ? `${statusCode} - ` : '(unknown status code) - ';
    message += title ? `${title} - ` : '(unknown error message) - ';
    message += detail ? `${JSON.stringify(detail)}` : '(unknown error detail)';

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
    throw new HttpError(error.response.status, error.response.statusText, error.response.data.detail)
  } else if (error.request) {
    throw new NetworkError('Impossible to contact the server. Check your internet connection.');
  } else {
    throw new UnexpectedError(`${error.message}`);
  }
}