package org.sagebionetworks.openchallenges.challenge.service.api;

import org.sagebionetworks.openchallenges.challenge.service.model.dto.ChallengePlatformDto;
import org.sagebionetworks.openchallenges.challenge.service.model.dto.ChallengePlatformsPageDto;
import org.sagebionetworks.openchallenges.challenge.service.service.ChallengePlatformService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;

@Component
public class ChallengePlatformApiDelegateImpl implements ChallengePlatformApiDelegate {

  @Autowired ChallengePlatformService challengePlatformService;

  @Override
  public ResponseEntity<ChallengePlatformDto> getChallengePlatform(String challengePlatformName) {
    return ResponseEntity.ok(challengePlatformService.getChallengePlatform(challengePlatformName));
  }

  @Override
  public ResponseEntity<ChallengePlatformsPageDto> listChallengePlatforms(
      Integer pageNumber, Integer pageSize) {
    return ResponseEntity.ok(challengePlatformService.listChallengePlatforms(pageNumber, pageSize));
  }
}