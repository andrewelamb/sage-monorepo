package org.sagebionetworks.openchallenges.challenge.service.api;

import org.sagebionetworks.openchallenges.challenge.service.model.dto.ChallengeInputDataTypesPageDto;
import org.sagebionetworks.openchallenges.challenge.service.service.ChallengeInputDataTypeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;

@Component
public class ChallengeInputDataTypeApiDelegateImpl implements ChallengeInputDataTypeApiDelegate {

  @Autowired ChallengeInputDataTypeService challengeInputDataTypeService;

  @Override
  public ResponseEntity<ChallengeInputDataTypesPageDto> listChallengeInputDataTypes(
      Integer pageNumber, Integer pageSize) {
    return ResponseEntity.ok(
        challengeInputDataTypeService.listChallengeInputDataTypes(pageNumber, pageSize));
  }
}