package org.sagebionetworks.openchallenges.challenge.service.model.mapper;

import org.sagebionetworks.openchallenges.challenge.service.model.dto.ChallengeInputDataTypeDto;
import org.sagebionetworks.openchallenges.challenge.service.model.entity.ChallengeInputDataTypeEntity;
import org.sagebionetworks.util.model.mapper.BaseMapper;
import org.springframework.beans.BeanUtils;

public class ChallengeInputDataTypeMapper
    extends BaseMapper<ChallengeInputDataTypeEntity, ChallengeInputDataTypeDto> {
  @Override
  public ChallengeInputDataTypeEntity convertToEntity(
      ChallengeInputDataTypeDto dto, Object... args) {
    ChallengeInputDataTypeEntity entity = new ChallengeInputDataTypeEntity();
    if (dto != null) {
      BeanUtils.copyProperties(dto, entity);
    }
    return entity;
  }

  @Override
  public ChallengeInputDataTypeDto convertToDto(
      ChallengeInputDataTypeEntity entity, Object... args) {
    ChallengeInputDataTypeDto dto = new ChallengeInputDataTypeDto();
    if (entity != null) {
      BeanUtils.copyProperties(entity, dto);
    }
    return dto;
  }
}
