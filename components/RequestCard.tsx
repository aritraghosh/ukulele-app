'use client';

import { SongRequest } from '@/types';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ThumbsUp } from 'lucide-react';

interface RequestCardProps {
  request: SongRequest;
  onVote: (id: string) => void;
  votingDisabled?: boolean;
}

export function RequestCard({ request, onVote, votingDisabled }: RequestCardProps) {
  return (
    <Card>
      <CardContent className="flex items-center justify-between py-4">
        <div>
          <p className="font-medium">{request.title}</p>
          <p className="text-sm text-muted-foreground">{request.artist}</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm font-semibold tabular-nums">{request.votes}</span>
          <Button
            variant={request.hasVoted ? 'default' : 'outline'}
            size="sm"
            onClick={() => onVote(request.id)}
            disabled={request.hasVoted || votingDisabled}
          >
            <ThumbsUp className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
