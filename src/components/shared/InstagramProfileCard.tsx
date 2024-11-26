// src/components/shared/InstagramProfileCard.tsx
import { type ReactElement } from "react";
import { Card, CardHeader } from "@/components/ui/card";
import { CheckCircle2 } from "lucide-react";
import type { InstagramProfile } from "@/types/instagram.types";

interface InstagramProfileCardProps {
  profile: InstagramProfile;
  isSelected?: boolean;
  onSelect?: (profile: InstagramProfile) => void;
  showStats?: boolean;
}

export function InstagramProfileCard({
  profile,
  isSelected = false,
  onSelect,
  showStats = true
}: InstagramProfileCardProps): ReactElement {
  const formatNumber = (num: number): string => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const handleClick = (): void => {
    onSelect?.(profile);
  };

  return (
    <Card
      className={`relative overflow-hidden transition-all duration-200 ${
        isSelected ? "ring-2 ring-blue-500" : ""
      }`}
      onClick={handleClick}
    >
      <CardHeader>
        <div className="flex items-center space-x-3">
          <div className="relative w-12 h-12">
            <img
              src={profile.profile_picture_url}
              alt={profile.username}
              className="rounded-full object-cover w-full h-full"
            />
          </div>
          <div className="flex flex-col flex-1 min-w-0">
            <div className="flex items-center gap-1">
              <p className="text-sm font-medium text-white truncate">
                {profile.username}
              </p>
              {profile.is_verified && (
                <CheckCircle2 className="w-4 h-4 text-blue-500" />
              )}
            </div>
            <p className="text-xs text-gray-400 truncate">{profile.full_name}</p>
          </div>
        </div>
        {showStats && (
          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="text-center">
              <p className="text-sm font-medium">Followers</p>
              <p className="text-lg">{formatNumber(profile.followers_count)}</p>
            </div>
            {profile.engagement_rate != null && (
              <div className="text-center">
                <p className="text-sm font-medium">Engagement</p>
                <p className="text-lg">{profile.engagement_rate.toFixed(1)}%</p>
              </div>
            )}
          </div>
        )}
      </CardHeader>
    </Card>
  );
}