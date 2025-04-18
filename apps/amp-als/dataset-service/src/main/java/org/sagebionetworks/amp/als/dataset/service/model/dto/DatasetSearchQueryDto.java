package org.sagebionetworks.amp.als.dataset.service.model.dto;

import java.net.URI;
import java.util.Objects;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonTypeName;
import org.sagebionetworks.amp.als.dataset.service.model.dto.DatasetDirectionDto;
import org.sagebionetworks.amp.als.dataset.service.model.dto.DatasetSortDto;
import java.time.OffsetDateTime;
import javax.validation.Valid;
import javax.validation.constraints.*;
import io.swagger.v3.oas.annotations.media.Schema;


import java.util.*;
import javax.annotation.Generated;

/**
 * A dataset search query.
 */

@Schema(name = "DatasetSearchQuery", description = "A dataset search query.")
@JsonTypeName("DatasetSearchQuery")
@Generated(value = "org.openapitools.codegen.languages.SpringCodegen")
// TODO Add x-java-class-annotations
public class DatasetSearchQueryDto {

  @JsonProperty("pageNumber")
  private Integer pageNumber = 0;

  @JsonProperty("pageSize")
  private Integer pageSize = 100;

  @JsonProperty("sort")
  private DatasetSortDto sort = DatasetSortDto.RELEVANCE;

  @JsonProperty("sortSeed")
  private Integer sortSeed = null;

  @JsonProperty("direction")
  private DatasetDirectionDto direction = null;

  @JsonProperty("searchTerms")
  private String searchTerms;

  public DatasetSearchQueryDto pageNumber(Integer pageNumber) {
    this.pageNumber = pageNumber;
    return this;
  }

  /**
   * The page number.
   * minimum: 0
   * @return pageNumber
  */
  @Min(0) 
  @Schema(name = "pageNumber", description = "The page number.", required = false)
  public Integer getPageNumber() {
    return pageNumber;
  }

  public void setPageNumber(Integer pageNumber) {
    this.pageNumber = pageNumber;
  }

  public DatasetSearchQueryDto pageSize(Integer pageSize) {
    this.pageSize = pageSize;
    return this;
  }

  /**
   * The number of items in a single page.
   * minimum: 1
   * @return pageSize
  */
  @Min(1) 
  @Schema(name = "pageSize", description = "The number of items in a single page.", required = false)
  public Integer getPageSize() {
    return pageSize;
  }

  public void setPageSize(Integer pageSize) {
    this.pageSize = pageSize;
  }

  public DatasetSearchQueryDto sort(DatasetSortDto sort) {
    this.sort = sort;
    return this;
  }

  /**
   * Get sort
   * @return sort
  */
  @Valid 
  @Schema(name = "sort", required = false)
  public DatasetSortDto getSort() {
    return sort;
  }

  public void setSort(DatasetSortDto sort) {
    this.sort = sort;
  }

  public DatasetSearchQueryDto sortSeed(Integer sortSeed) {
    this.sortSeed = sortSeed;
    return this;
  }

  /**
   * The seed that initializes the random sorter.
   * minimum: 0
   * maximum: 2147483647
   * @return sortSeed
  */
  @Min(0) @Max(2147483647) 
  @Schema(name = "sortSeed", description = "The seed that initializes the random sorter.", required = false)
  public Integer getSortSeed() {
    return sortSeed;
  }

  public void setSortSeed(Integer sortSeed) {
    this.sortSeed = sortSeed;
  }

  public DatasetSearchQueryDto direction(DatasetDirectionDto direction) {
    this.direction = direction;
    return this;
  }

  /**
   * Get direction
   * @return direction
  */
  @Valid 
  @Schema(name = "direction", required = false)
  public DatasetDirectionDto getDirection() {
    return direction;
  }

  public void setDirection(DatasetDirectionDto direction) {
    this.direction = direction;
  }

  public DatasetSearchQueryDto searchTerms(String searchTerms) {
    this.searchTerms = searchTerms;
    return this;
  }

  /**
   * A string of search terms used to filter the results.
   * @return searchTerms
  */
  
  @Schema(name = "searchTerms", example = "clinical", description = "A string of search terms used to filter the results.", required = false)
  public String getSearchTerms() {
    return searchTerms;
  }

  public void setSearchTerms(String searchTerms) {
    this.searchTerms = searchTerms;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    DatasetSearchQueryDto datasetSearchQuery = (DatasetSearchQueryDto) o;
    return Objects.equals(this.pageNumber, datasetSearchQuery.pageNumber) &&
        Objects.equals(this.pageSize, datasetSearchQuery.pageSize) &&
        Objects.equals(this.sort, datasetSearchQuery.sort) &&
        Objects.equals(this.sortSeed, datasetSearchQuery.sortSeed) &&
        Objects.equals(this.direction, datasetSearchQuery.direction) &&
        Objects.equals(this.searchTerms, datasetSearchQuery.searchTerms);
  }

  @Override
  public int hashCode() {
    return Objects.hash(pageNumber, pageSize, sort, sortSeed, direction, searchTerms);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class DatasetSearchQueryDto {\n");
    sb.append("    pageNumber: ").append(toIndentedString(pageNumber)).append("\n");
    sb.append("    pageSize: ").append(toIndentedString(pageSize)).append("\n");
    sb.append("    sort: ").append(toIndentedString(sort)).append("\n");
    sb.append("    sortSeed: ").append(toIndentedString(sortSeed)).append("\n");
    sb.append("    direction: ").append(toIndentedString(direction)).append("\n");
    sb.append("    searchTerms: ").append(toIndentedString(searchTerms)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }
}

