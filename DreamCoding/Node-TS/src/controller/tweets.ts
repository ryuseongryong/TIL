import { Request, Response } from 'express';
import * as tweetsRepository from '../data/tweets';
export async function getTweets(req: Request, res: Response): Promise<void> {
  const tweets = await tweetsRepository.getAll();
  res.status(200).json(tweets);
}
